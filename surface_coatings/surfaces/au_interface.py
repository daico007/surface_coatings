"""Routine to create graphene surface"""
import mbuild as mb
import numpy as np


class AuLattice(mb.Compound):
    """A general gold surface recipe exposed to vacuum.


    Parameters
    ----------
    x : int, default=4
        dimensions of gold sheet length in nm
    y : int, default=4
        dimensions of gold sheet depth in nm
    n_layers : int, default=3
        number of layers of gold cells

    Attributes
    ----------
    see mbuild.Compound

    """
    def __init__(self, x=5, y=5, n_layers=3):
        super(AuLattice, self).__init__()

        # Estimate the number of lattice repeat units
        replicate = [int(x/0.40782), int(y/0.40782)]
        if all(x <= 0 for x in [x, y]):
            msg = 'Dimension of graphene sheet must be greater than zero'
            raise ValueError(msg)
        au = mb.Compound(name='Au', element='Au')
        # full Au cell position (face center)
        # au_locations = [
        #     [0, 0, 0], [1, 0, 0], [0, 1, 0], [1, 1, 0], [0.5, 0.5, 0],
        #     [0, 0.5, 0.5], [1, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 1, 0.5],
        #     [0, 0, 1], [1, 0, 1], [0, 1, 1], [1, 1, 1], [0.5, 0.5, 1]
        # ]

        au_locations = [
            [0, 0, 0], [0.5, 0.5, 0],
            [0, 0.5, 0.5], [0.5, 0, 0.5],
        ]
        basis = {au.name: au_locations}
        lattice_spacing = [0.40782, 0.40782, 0.40782]
        angles = [90.0, 90.0, 90.0]

        au_lattice = mb.Lattice(lattice_spacing=lattice_spacing,
                                      angles=angles, lattice_points=basis)

        au_sheet = au_lattice.populate(compound_dict={au.name: au},
                                             x=replicate[0], y=replicate[1],
                                             z=n_layers)


        self.add(au_sheet)

        self.xyz -= np.min(self.xyz, axis=0)
        self.xyz -= np.min(self.xyz, axis=0)

        self.periodicity = (True, True, True)