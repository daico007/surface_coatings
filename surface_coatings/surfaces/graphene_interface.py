"""Routine to create graphene surface"""
import mbuild as mb
import numpy as np


class GrapheneInterface(mb.Compound):
    """A general graphene surface recipe exposed to vacuum.

    This class is adapted from
    https://github.com/PTC-CMC/Pore-Builder/blob/master/porebuilder/porebuilder.py
    Parameters
    ----------
    x_length : int, default=4
        dimensions of graphene sheet length in nm
    y_length : int, default=4
        dimensions of graphene sheet depth in nm
    n_sheets : int, default=3
        number of parallel graphene sheets
    vacuum : float, default=10.0
        Dimension of vacuum space in z-direction in nm

    Attributes
    ----------
    see mbuild.Compound

    """
    def __init__(self, x_length=4, y_length=3, n_sheets=3, vacuumn=10.0):
        super(GrapheneInterface, self).__init__()

        factor = np.cos(np.pi/6)
        # Estimate the number of lattice repeat units
        replicate = [int(x_length/0.2456), (y_length/0.2456)*(1/factor)]
        if all(x <= 0 for x in [x_length, y_length]):
            msg = 'Dimension of graphene sheet must be greater than zero'
            raise ValueError(msg)
        carbon = mb.Compound()
        carbon.name = 'C'
        carbon_locations = [[0, 0, 0], [2/3, 1/3, 0]]
        basis = {carbon.name: carbon_locations}
        lattice_spacing = [0.2456, 0.2456, 0.335]
        angles = [90.0, 90.0, 120.0]

        graphene_lattice = mb.Lattice(lattice_spacing=lattice_spacing,
                                      angles=angles, lattice_points=basis)

        graphene = graphene_lattice.populate(compound_dict={carbon.name: carbon},
                                             x=replicate[0], y=replicate[1],
                                             z=1)

        for particle in graphene.particles():
            if particle.xyz[0][0] < 0:
                particle.xyz[0][0] += graphene.box.Lx

        self.add(graphene)
        self.xyz -= np.min(self.xyz, axis=0)

        self.xyz -= np.min(self.xyz, axis=0)