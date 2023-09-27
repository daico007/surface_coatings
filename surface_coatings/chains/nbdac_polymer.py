"""Routine to create nBDAC polymer."""
import warnings

import mbuild as mb
import numpy as np
from mbuild.lib.atoms import H
from mbuild.lib.moieties import CH2, Silane
from mbuild.lib.recipes import Polymer

from surface_coatings.monomers import mNBDAC
from surface_coatings.monomers.mnbdac.side_chains import AminoPropyl
from surface_coatings.monomers.mnbdac.terminal_groups import Acetaldehyde


class O(mb.Compound):
    """An oxygen with two ports attached."""
    def __init__(self):
        super(O, self).__init__()
        oxygen = mb.Compound(name="O", element="O")
        self.add(oxygen)
        self.add(mb.Port(anchor=self[0]), "up")
        self["up"].translate([0, 0.07, 0])

        self.add(mb.Port(anchor=self[0]), "down")
        self["down"].translate([0, -0.07, 0])

class fmNBDAC(mb.Compound):
    """Functionalized NBDAC monomer.

    Parameters
    ----------
    side_chains : mb.Compound or list of Compounds (len 2)
        Side chains attached to the NBDAC monomer
    terminal_groups : mb.Compound or list of Compounds (len 2)
        Terminal groups which will be matched side chains
    """

    def __init__(
        self, side_chains=AminoPropyl(), terminal_groups=Acetaldehyde()
    ):
        super(fmNBDAC, self).__init__()
        if isinstance(side_chains, list):
            assert all(
                isinstance(side_chain, mb.Compound)
                for side_chain in side_chains
            )
        elif isinstance(side_chains, mb.Compound):
            side_chains = [mb.clone(side_chains), mb.clone(side_chains)]

        if isinstance(terminal_groups, list):
            assert all(
                isinstance(terminal_groups, mb.Compound)
                for terminal_group in terminal_groups
            )
        elif isinstance(terminal_groups, mb.Compound):
            terminal_groups = [
                mb.clone(terminal_groups),
                mb.clone(terminal_groups),
            ]

        backbone = mNBDAC()
        self.add(backbone)
        self.add(side_chains)
        self.add(terminal_groups)

        for i in range(2):
            mb.force_overlap(
                move_this=side_chains[i],
                from_positions=side_chains[i]["side"],
                to_positions=backbone[f"side{i}"],
            )

            assert side_chains[i].labels.get("terminal")
            mb.force_overlap(
                move_this=terminal_groups[i],
                from_positions=terminal_groups[i]["terminal"],
                to_positions=side_chains[i]["terminal"],
            )

        self.labels["up"] = backbone["up"]
        self.labels["down"] = backbone["down"]


class pNBDAC(mb.Compound):
    """A general method to create a NBDAC polymer with varying side chains/terminal groups.

    Parameters
    ----------
    side_chains : mb.Compound or list of Compounds (len 2)
        Side chains attached to NBDAC monomer
    terminal_groups: mb.Compound or list of Compounds (len 2)
        Terminal groups which will be matched with side chains
    cap_front : bool, optional, default=True
        Cap the front of the polymer (NBDAC end)
    cap_end : bool, optional, default=False
        Cap the end of the polymer (Silane end)
    buffer : str, optional, default=None
        Type of buffer to be attached to the end of the pNBDAC.
        Available options: None, "alkyl", "ether", "silane"
    buffer_length : int, optional, default=1
        Length of CH2 monomer to be added to the buffer at one end of the NBDAC polymer
    n : int, optional, default=1
        Number of repeat for the monomer
    port_labels: tuple, optional, default=('up', 'down')
        The list of ports of the monomers. The Silane will connect with the first port
        and the last port will be capped by a Hydrogen
    algin : bool, optional, default=True
        If True, align the port connected to the silane buffer with the rest of the polymer.
        The goal is to create a straight polymer when grafted on a surface.
    """

    def __init__(
        self,
        monomer,
        side_chains=AminoPropyl(),
        terminal_groups=Acetaldehyde(),
        buffer=None,
        buffer_length=1,
        cap_front=True,
        cap_end=False,
        n=1,
        port_labels=("up", "down"),
        align=True,
    ):
        super(pNBDAC, self).__init__()
        if monomer:
            assert isinstance(monomer, fmNBDAC)
            if side_chains and terminal_groups:
                warnings.warn(
                    "Both monomer and (side_chains, terminal_groups) are provided,"
                    "only monomer will be used to construct the polymer."
                    "Please refer to docstring for more information."
                )
        else:
            monomer = fmNBDAC(side_chains, terminal_groups)

        polymer = Polymer(monomers=[monomer])
        polymer.build(n=n, add_hydrogens=False)
        self.add(polymer, "Polymer")

        if buffer:
            tail = mb.Compound(name="tail")
            buffer_options = {"alkyl": CH2,
                              "ether": O,
                              "silane": Silane}
            tail.add(buffer_options.get(buffer.lower())(), "Buffer")
            tail.add(CH2(), "CH2_0")

            i = 0
            for i in range(buffer_length):
                tail.add(CH2(), f"CH2_{i+1}")
                mb.force_overlap(
                    tail[f"CH2_{i+1}"],
                    tail[f"CH2_{i+1}"]["down"],
                    tail[f"CH2_{i}"]["up"],
                )

            mb.force_overlap(
                tail["Buffer"], tail["Buffer"]["up"], tail[f"CH2_0"]["down"]
            )

            self.add(tail, "tail")

            if align:
                polymer_vector = (
                    polymer[port_labels[1]].anchor.pos
                    - polymer[port_labels[0]].anchor.pos
                )
                norm_vector = polymer_vector / np.linalg.norm(polymer_vector)

                polymer[port_labels[0]].update_orientation(
                    orientation=norm_vector
                )

            mb.force_overlap(
                tail, tail[f"CH2_{i+1}"]["up"], polymer[port_labels[0]]
            )

            self.labels["up"] = self["Polymer"][port_labels[1]]
            self.labels["down"] = self["tail"]["Buffer"]["down"]
        else:
            self.labels["up"] = self["Polymer"]["up"]
            self.labels["down"] = self["Polymer"]["down"]

        if cap_front:
            front_cap = H()
            self.add(front_cap, "front_cap")
            mb.force_overlap(
                move_this=front_cap,
                from_positions=front_cap["up"],
                to_positions=self["up"],
            )
        if cap_end:
            end_cap = H()
            self.add(end_cap, "end_cap")
            mb.force_overlap(
                move_this=end_cap,
                from_positions=end_cap["up"],
                to_positions=self["down"],
            )
