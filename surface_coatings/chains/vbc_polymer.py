"""Routine to create VBC polymer."""
import mbuild as mb
from mbuild.lib.recipes import Polymer
import numpy as np

from surface_coatings.monomers import MethylStyrene
from surface_coatings.monomers import (AzPMA, SBMA, Methacrylate, TriazoleBiotin)


class VBCPolymer(mb.Compound):
    def __init__(self, monomers=[Methacrylate(), SBMA(), AzPMA(), TriazoleBiotin()], n=1,
                 sequence='AABCBBD', port_labels=('up', 'down')):
        """This is a general method to create a Vinylbenzyl Polymer

        Parameters
        ----------
        monomers: list of monomer
            List of monomers to be connected together
        n: int, optional, default=1
            Number of repeat for the polymer
        sequence: str
            The sequence of all the monomer, corresponding to the monomers list
        port_labels: tuple, optional, default=('up', 'down')
            The list ports of the monomers. The VBC will connect to the first port,
            and the last port will be capped by a Hydrogen
        """
        super(VBCPolymer, self).__init__()
        polymer = Polymer(monomers=monomers)
        polymer.build(n=n, sequence=sequence, add_hydrogens=False)
        self.add(polymer, label="Polymer")
        vbc = MethylStyrene()
        self.add(vbc, label="VBC")
        mb.force_overlap(vbc,
                         vbc['up'],
                         polymer[port_labels[0]])
        for port in self.all_ports():
            if port.access_labels:
                self.labels['up'] = port
            else:
                self.labels['down'] = port

        orientation = self['Polymer']['down'].direction
        for port in self.available_ports():
            if not all(np.isclose(port.direction, orientation)):
                port.update_orientation(-orientation)
