from copy import deepcopy
from warnings import warn

import numpy as np

import mbuild as mb
from mbuild.lib.atoms import H
from mbuild.lib.moieties import H2O
from mbuild.lib.recipes import Monolayer


class Monolayer(mb.Compound):
    """A general monolayer recipe.

    Parameters
    ----------

    """
    def __init__(self, surface, chain, backfill, pattern, tile_x=1, tile_y=1, rotate=True, seed=12345, **kwargs):
        super(Monolayer, self).__init__()

        tile_compound = mb.lib.recipes.TiledCompound(surface, n_tiles=(tile_x, tile_y, 1))
        self.add(tile_compound, label="tiled_surface")

        if pattern is None:
            pattern = mb.Random2DPattern(len(tiled_compound.reference_ports()))

            attached_chains, backills = pattern.apply_to_compound(gues=chain,
                                                                  host=self["tiled_surface"],
                                                                  backfill=backfill)