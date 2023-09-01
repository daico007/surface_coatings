"""Routines to construct solvated (dual) monolayer."""
from os import system

import mbuild as mb
import numpy as np
from mbuild.lib.moieties import H2O
from mbuild.packing import solvate


class SolvatedMonolayer(mb.Compound):
    """Solvated monolayer system.

    Parameters
    ----------
    monolayer: mb.Compound
        The monolayer to be solvated.
    solvent: mb.Compound, optional, default=H2O()
        The solvent to be used.
    n_solvents: int, optional, default=1000
        The number of solvent compounds used.
    solvent_box_height: float, optional, default=5
        The height of the solvent box. The base of the box adapt those of the monolayer/surface.
    seed: int, optional, default=12345
        Random seed used for any subprocess.
    """

    def __init__(
        self,
        monolayer,
        solvent=H2O(),
        n_solvents=1000,
        solvent_box_height=5,
        seed=12345,
    ):
        super(SolvatedMonolayer, self).__init__()
        monolayer_box_lengths = monolayer.get_boundingbox().lengths
        surface_box_lengths = (
            monolayer["tiled_surface"].get_boundingbox().lengths
        )
        # Calculate surface coords
        xs, ys, zs = list(), list(), list()
        for pos in monolayer["tiled_surface"].xyz:
            xs.append(pos[0]), ys.append(pos[1]), zs.append(pos[2])
        xs.sort(), ys.sort(), zs.sort()
        surface_bounding_coords = (
            (xs[0], xs[-1]),
            (ys[0], ys[-1]),
            (zs[0], zs[-1]),
        )

        # Change this to solvating the whole system using the solvate method.
        solvent_box = [
            surface_box_lengths[0],
            surface_box_lengths[1],
            solvent_box_height,
        ]
        box_of_solvent = mb.fill_box(
            compound=solvent, box=solvent_box, n_compounds=n_solvents
        )
        box_of_solvent.translate(
            [
                surface_bounding_coords[0][0],
                surface_bounding_coords[1][0],
                monolayer_box_lengths[2],
            ]
        )
        self.add(monolayer, label="monolayer")
        self.add(box_of_solvent, label="solvent")

        system_box_lengths = [
            monolayer_box_lengths[0],
            monolayer_box_lengths[1],
            monolayer_box_lengths[2] + solvent_box_height,
        ]
        self.box = mb.Box(system_box_lengths)
        self.periodicity = monolayer.periodicity


class SolvatedDualMonolayer(mb.Compound):
    """Solvated dual-monolayer system.

    Parameters
    ----------
    dual_monolayer: mb.Compound
        The dual-monolayer system to be solvated.
    solvent: mb.Compound, optional, default=H2O()
        The solvent compound to be used.
    n_solvents: int, optional, n=1000
        The number of solvent molecules to be used.
    seed: int, optional, default=12345
        Random seed used for any subprocess.
    """

    def __init__(
        self, dual_monolayer, solvent=H2O(), n_solvents=1000, seed=12345
    ):
        super(SolvatedDualMonolayer, self).__init__()
        top_monolayer = dual_monolayer["top_monolayer"]
        top_monolayer_box_lengths = top_monolayer.get_boundingbox().lengths
        top_surface_box_lenghts = (
            top_monolayer["tiled_surface"].get_boundingbox().lengths
        )

        bottom_monolayer = dual_monolayer["bottom_monolayer"]
        bottom_monolayer_box_lengths = (
            bottom_monolayer.get_boundingbox().lengths
        )

        # Calculate surface coords
        xs, ys, zs = list(), list(), list()
        for pos in bottom_monolayer["tiled_surface"].xyz:
            xs.append(pos[0]), ys.append(pos[1]), zs.append(pos[2])
        xs.sort(), ys.sort(), zs.sort()
        bottom_surface_coords = (
            (xs[0], xs[-1]),
            (ys[0], ys[-1]),
            (zs[0], zs[-1]),
        )
        bottom_surface_box_lengths = (
            bottom_monolayer["tiled_surface"].get_boundingbox().lengths
        )

        dual_monolayer_box_lengths = dual_monolayer.get_boundingbox().lengths

        separation = dual_monolayer_box_lengths[2] - (
            top_monolayer_box_lengths[2] + bottom_monolayer_box_lengths[2]
        )
        solvent_box = [
            bottom_surface_box_lengths[0],
            bottom_surface_box_lengths[1],
            separation,
        ]
        box_of_solvent = mb.fill_box(
            compound=solvent, box=solvent_box, n_compounds=n_solvents
        )
        box_of_solvent.translate(
            [
                bottom_surface_coords[0][0],
                bottom_surface_coords[1][0],
                bottom_monolayer_box_lengths[2],
            ]
        )
        self.add(dual_monolayer, label="monolayers")
        self.add(box_of_solvent, label="solvents")

        system_box_lengths = [
            max(top_surface_box_lenghts[0], bottom_surface_box_lengths[0]),
            max(top_surface_box_lenghts[1], bottom_surface_box_lengths[1]),
            self.get_boundingbox().lengths[2],
        ]
        self.box = mb.Box(system_box_lengths)
        self.periodicity = bottom_monolayer.periodicity
