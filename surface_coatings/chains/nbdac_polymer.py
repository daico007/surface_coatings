"""Routine to create nBDAC polymer."""

import mbuild as mb
from mbuild.lib.recipes import Polymer
from mbuild.lib.moieties import Silane
from mbuild.lib.atoms import H

from surface_coatings.monomers import mNBDAC
from surface_coatings.monomers.mnbdac.side_chains import AminoPropyl
from surface_coatings.monomers.mnbdac.terminal_groups import Acetaldehyde

import warnings

class fmNBDAC(mb.Compound):
    def __init__(self, side_chains=AminoPropyl(), terminal_groups=Acetaldehyde()):
        """Functionalized NBDAC monomer.

        Parameters
        ----------
        side_chains : mb.Compound or list of Compounds (len 2)
            Side chains attached to the NBDAC monomer
        terminal_groups : mb.Compound or list of Compounds (len 2)
            Terminal groups which will be matched side chains
        """
        super(fmNBDAC, self).__init__()
        if isinstance(side_chains, list):
            assert all(isinstance(side_chain, mb.Compound) for side_chain in side_chains)
        elif isinstance(side_chains, mb.Compound):
            side_chains = [mb.clone(side_chains), mb.clone(side_chains)]

        if isinstance(terminal_groups, list):
            assert all(isinstance(terminal_groups, mb.Compound) for terminal_group in terminal_groups)
        elif isinstance(terminal_groups, mb.Compound):
            terminal_groups = [mb.clone(terminal_groups), mb.clone(terminal_groups)]

        backbone = mNBDAC()
        self.add(backbone)
        self.add(side_chains)
        self.add(terminal_groups)

        for i in range(2):
            mb.force_overlap(move_this=side_chains[i],
                             from_positions=side_chains[i]["side"],
                             to_positions=backbone[f"side{i}"])

            assert side_chains[i].labels.get("terminal")
            mb.force_overlap(move_this=terminal_groups[i],
                             from_positions=terminal_groups[i]["terminal"],
                             to_positions=side_chains[i]["terminal"])

        self.labels["up"] = backbone["up"]
        self.labels["down"] = backbone["down"]


class pNBDAC(mb.Compound):
    def __init__(self, monomer, side_chains=AminoPropyl(), terminal_groups=Acetaldehyde(),
                 silane_buffer=True, cap=None, n=1, port_labels=('up', 'down')):
        """This is a general method to create a NBDAC polymer with varying side chains/terminal groups.

        Parameters
        ----------
        side_chains : mb.Compound or list of Compounds (len 2)
            Side chains attached to NBDAC monomer
        terminal_groups: mb.Compound or list of Compounds (len 2)
            Terminal groups which will be matched with side chains
        silane_buffer : int, optional, default=1
            Silane monomer used to buffer at one end of the NBDAC polymer
        n : int, optional, default=1
            Number of repeat for the monomer
        port_labels: tuple, optional, default=('up', 'down')
            The list of ports of the monomers. The Silane will connect with the first port
            and the last port will be capped by a Hydrogen
        """
        super(pNBDAC, self).__init__()
        if monomer:
            assert isinstance(monomer, fmNBDAC)
            if side_chains and terminal_groups:
                warnings.warn("Both monomer and (side_chains, terminal_groups) are provided,"
                              "only monomer will be used to construct the polymer."
                              "Please refer to docstring for more information.")
        else:
            monomer = fmNBDAC(side_chains, terminal_groups)

        polymer = Polymer(monomers=[monomer])
        polymer.build(n=n, add_hydrogens=False)
        self.add(polymer, "Polymer")

        if silane_buffer:
            silane = Silane()
            self.add(silane, label="Silane")
            mb.force_overlap(silane,
                             silane['up'],
                             polymer[port_labels[0]])

            self.labels["up"] = self["Polymer"]["down"]
            self.labels["down"] = self["Silane"]["down"]
        else:
            self.labels["up"] = self["Polymer"]["up"]
            self.labels["down"] = self["Polymer"]["down"]

        if cap:
            if isinstance(cap, mb.Compound):
                mb.force_overlap(move_this=cap,
                                 from_positions=cap["up"],
                                 to_positions=self["down"])


