from copy import deepcopy
from warnings import warn

import numpy as np

import mbuild as mb
from mbuild.lib.atoms import H
from mbuild.lib.recipes import Monolayer


class Monolayer(mb.Compound):
    """A general monolayer recipe.

    Parameters
    ----------

    """
    def __init__(self, surface, chain, n_chains, backfill, tile_x=1, tile_y=1, rotate=True, seed=12345, **kwargs):
        super(Monolayer, self).__init__()

        tiled_compound = mb.lib.recipes.TiledCompound(surface, n_tiles=(tile_x, tile_y, 1))
        self.add(tiled_compound, label="tiled_surface")

        pattern = mb.Random2DPattern(n_chains, seed=seed)

        # Attach final chains, remaining sites get a backfill)
        attached_chains, backills = pattern.apply_to_compound(guest=chain,
                                                              host=self["tiled_surface"],
                                                              backfill=backfill,
                                                              **kwargs)
        self.add(attached_chains)
        self.add(backills)

        if rotate:
            np.random.seed(seed)
            for chain in attached_chains:
                rotation = np.random.random() * np.pi * 2.0
                chain.spin(rotation, [0, 0, 1])

        self.periodicity = [True, True, False]