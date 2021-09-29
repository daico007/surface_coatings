"""Routines to create (dual) monolayer systems."""
from copy import deepcopy
from warnings import warn

import numpy as np

import mbuild as mb
from mbuild.exceptions import MBuildError
from mbuild.lib.atoms import H


class Monolayer(mb.Compound):
    """A surface coated by a monolayer.

    Parameters
    ----------
    surface: mb.Compound
        The surface with ports at its surface.
    chains: list of mb.Compound
        The chains that are to be attached to the surface.
    n_chains: int
        The number of chains to be attached.
    fractions: list of fraction of floats, default=None
        The list of fractions to fill for each compound in `chains`. If 
        the value is not specified, the chains will be proportional on 
        the surface.
    backfill: mb.Compound, optional, default=H()
        Compound used to backfill leftover ports (after all chains have been attached.
    tile_x, tile_y: int, optional, default= 1, 1
        The number of surface tiles.
    rotate_chains: bool, optional, default=True
        Options to rotate the chain randomly.
    seed: int, optional, default= 12345
        Random seed used for any subprocess.
    """
    def __init__(self, surface, chains, n_chains, fractions=None, backfill=H(), tile_x=1, tile_y=1, rotate_chains=True, seed=12345, **kwargs):
        super(Monolayer, self).__init__()

        tiled_compound = mb.lib.recipes.TiledCompound(surface, n_tiles=(tile_x, tile_y, 1))
        self.add(tiled_compound, label="tiled_surface")

        pattern = mb.Random2DPattern(n_chains, seed=seed)

        if not isinstance(chains, list):
            chains=list(chains)
        if not isinstance(chains[0], mb.Compound):
            raise MBuildError("Please provide chains as a list of mbuild.Compounds")
        if not fractions:
            fractions = [1 / len(chains) for _ in range(len(chains))]
        if isinstance(fractions, float):
            fractions=list(fractions)
        elif not isinstance(fractions, list):
            raise TypeError("fractions has been provided as type {}. Please provide a list of floats.".format(type(fractions)))
        if len(chains) != len(fractions):
            raise ValueError("Number of fractions does not match the number of chain types provided.")

        # Attach final chains, remaining sites get a backfill)
        # Attach chains of each type to binding sites based on
        # respective fractions.
        if len(chains) > 1:
            for chain, fraction in zip(chains[:-1], fractions[:-1]):
                # Create sub-pattern for this chain type
                subpattern = deepcopy(pattern)
                n_points = int(round(fraction * n_chains))
                warn("\n Adding {} of chain {}".format(n_points, chain))
                pick = np.random.choice(subpattern.points.shape[0], n_points,
                                        replace=False)
                points = subpattern.points[pick]
                subpattern.points = points

                # Remove now-occupied points from overall pattern
                pattern.points = np.array([point for point in pattern.points.tolist()
                                           if point not in subpattern.points.tolist()])

                # Attach chains to the surface
                attached_chains, _ = subpattern.apply_to_compound(
                    guest=chain, host=self['tiled_surface'], backfill=None, **kwargs)
                self.add(attached_chains)

        else:
            warn("\n No fractions provided. Assuming a single chain type.")
        
        
        attached_chains, backills = pattern.apply_to_compound(guest=chains[-1],
                                                              host=self["tiled_surface"],
                                                              backfill=backfill,
                                                              **kwargs)
        self.add(attached_chains)
        self.add(backills)

        if rotate_chains:
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

        bot_box = bottom.get_boundingbox()
        z_val = bot_box.lengths[2]
        top.translate([0, 0, z_val + separation])
        if top.name and bottom.name:
            self.add(top, label=top.name)
            self.add(bottom, label=bottom.name)
        else:
            self.add(top, label="top_monolayer")
            self.add(bottom, label="bottom_monolayer")
