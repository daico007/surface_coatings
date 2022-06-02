"""Routine to create Silane polymer."""

import mbuild as mb
from mbuild.lib.recipes import Polymer
import numpy as np

from mbuild.lib.moieties import Silane
from surface_coatings.monomers import MPC


class SilanePolymer(mb.Compound):
    def __init__(self, monomers=[MPC()], n=1, sequence="A", port_labels=('up', 'down')):
        """This is a general method to create a Silane-ended/initiated Polymer

        Parameters
        ----------
        monomers: list of monomer
            List of monomers to be connected to get connected together
        n: int, optional, defautl=1
            Number of repeat for the monomer
        sequence: str
            The sequence of all the monomer, corresponding ot the monomers list
        port_labels: tuple, optional, default=('up', 'donw')
            The list of ports of the monomers. The Silane will connect to the first port
            and the last port will be capped by a Hydrogen.
        """
        super(SilanePolymer, self).__init__()
        polymer = Polymer(monomers=monomers)
        polymer.build(n=n, sequence=sequence, add_hydrogens=False)
        self.add(polymer, label="Polymer")
        silane = Silane()
        self.add(silane, label="Silane")
        mb.force_overlap(silane,
                         silane['up'],
                         polymer[port_labels[0]])

        self.labels["up"] = self["Polymer"]["down"]
        self.labels["down"] = self["Silane"]["down"]
