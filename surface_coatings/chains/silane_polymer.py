"""Routine to create Silane polymer."""

import mbuild as mb
from mbuild.lib.recipes import Polymer
import numpy as np

from mbuild.lib.atoms import H
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
            and the last port will be capped by a Hydrogen
        """
        super(SilanePolymer, self).__init__()
        end_groups = [H(), Silane()]
        polymer = Polymer(monomers=monomers, end_groups=end_groups)
        polymer.build(n=n, sequence=sequence, add_hydrogens=False)
        self.add(polymer, label="Polymer")
        for i in range(n):
            assert polymer.children[i] not in end_groups
            polymer.children[i].rotate(theta=2 * i * np.pi / n, around=[0, 1, 0])

        si = list(self.particles_by_name("Si"))[0]
        port = mb.Port(anchor=si, orientation=[0, -1, 0], separation=0.07)
        self.add(port, "down")