"""Routine to create Silane polymer."""

import mbuild as mb
from mbuild.lib.recipes import Polymer
import numpy as np

from mbuild.lib.atoms import H
from mbuild.lib.moieties import Silane
from surface_coatings.monomers import MPC


class SilanePolymer(mb.Compound):
    def __init__(self, monomers=[MPC()], n=1, sequence="A", initiator=None, port_labels=('up', 'down')):
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
        if initiator:
            silane = Silane()
            surface_end = mb.Compound([silane, initiator
            ])
            mb.force_overlap(move_this=silane,
                             from_positions=silane[port_labels[0]],
                             to_positions=initiator[port_labels[1]])
            surface_end.labels["up"] = surface_end[f"{initiator.name}[0]"]["up"]
            surface_end.labels["down"] = surface_end["Silane[0]"]["down"]
        else:
            surface_end = Silane()

        end_groups = [H(), surface_end]
        polymer = Polymer(monomers=monomers, end_groups=end_groups)
        polymer.build(n=n, sequence=sequence, add_hydrogens=False)
        self.add(polymer, label="Polymer")
        for i in range(n):
            assert polymer.children[i] not in end_groups
            polymer.children[i].rotate(theta=2 * i * np.pi / n, around=[0, 1, 0])

        si = list(self.particles_by_name("Si"))[0]
        port = mb.Port(anchor=si, orientation=[0, -1, 0], separation=0.07)
        self.add(port, port_labels[1])
