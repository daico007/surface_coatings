"""Routines to create (dual) monolayer systems."""
import numpy as np

import mbuild as mb
from mbuild.lib.atoms import H


class Monolayer(mb.Compound):
    """A surface coated by a monolayer.

    Parameters
    ----------
    surface: mb.Compound
        The surface with ports at its surface.
    chain: mb.Compound
        The chain that to be attached to the surfaces.
    n_chains: int
        The number of chains to be attached.
    backfill: mb.Compound, optional, default=H()
        Compound used to backfill leftover ports (after all chains have been attached.
    tile_x, tile_y: int, optional, default= 1, 1
        The number of surface tiles.
    rotate: bool, optional, default=True
        Options to rotate the chain randomly.
    seed: int, optional, default= 12345
        Random seed used for any subprocess.
    """
    def __init__(self, surface, chain, n_chains, backfill=H(), tile_x=1, tile_y=1, rotate=True, seed=12345, **kwargs):
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

        self.periodicity = surface.periodicity


class DualMonolayer(mb.Compound):
    """A dual-monolayer system.

    Parameters
    ----------
    top: mb.Compound
        The top surfaces of the dual-monolayer.
    bottom: mb.Compound
        The bottom surface of the dual-monolayer.
    separation: float, optional, default=0.8
        The separation between the two surfaces.
    """
    def __init__(self, top, bottom, separation=0.8):
        super(DualMonolayer, self).__init__()
        top.spin(np.pi, around=[0, 1, 0])
        top_box = top.get_boundingbox()
        bot_box = bottom.get_boundingbox()

        z_val = bot_box.lengths[2]

        top.translate([0, 0, z_val + separation])
        self.add(top, label="top_monolayer")
        self.add(bottom, label="bottom_monolayer")