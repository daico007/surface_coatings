import numpy as np
import mbuild as mb
from surface_coatings.monomers.methylstyrene import MethylStyrene


class CrystalineSilicon(mb.Compound):
    def __init__(self, x=10, y=10, z=10):
        super(CrystalineSilicon, self).__init__()
        # define all necessary lattice parameters
        spacings = [0.54309, 0.54309, 0.54309]
        angles = [90, 90, 90]

        points = [[0, 0, 0], [0.5, 0.5, 0], [0.5, 0, 0.5], [0, 0.5, 0.5],
                  [0.25, 0.25, 0.75], [0.25, 0.75, 0.25], [0.75, 0.25, 0.25], [0.75, 0.75, 0.75]]

        # define lattice object
        diamond_lattice = mb.Lattice(lattice_spacing=spacings,
                                     angles=angles, 
                                     lattice_points={'A': points})

        # define Compound
        si = mb.Compound(name='Si', element='Si')

        # populate lattice with compounds
        si_lattice = diamond_lattice.populate(compound_dict={'A' : si}, x=x, y=y, z=z)
        si_lattice.periodicity = [True, True, False]
        si_lattice.generate_bonds(name_a='Si', name_b='Si', dmin=0, dmax=0.236)
        self.add(si_lattice)
        self.periodicity = si_lattice.periodicity


class SiliconInterface(mb.Compound):
    def __init__(self, silicon=CrystalineSilicon(x=10, y=10, z=2), tile_x=1, tile_y=1, seed=12345):
        super(SiliconInterface, self).__init__()
        tiled_compound = mb.lib.recipes.TiledCompound(mb.clone(silicon), n_tiles=(tile_x, tile_y, 1))
        self.add(tiled_compound)
        self._identify_surface_sites()
        self.spin(np.pi, [0, 1, 0])
        self.periodicity = silicon.periodicity

    def _identify_surface_sites(self):
        for particle in list(self.particles()):
            if np.isclose(particle.pos[2], 0):
                label = f'Si_{len(self.referenced_ports())}'
                self.add(mb.Port(anchor=particle, orientation=[0, 0, -1], separation=0.09), label=label)

