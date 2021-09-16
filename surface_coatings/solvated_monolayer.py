import numpy as np
import mbuild as mb
from mbuild.lib.moieties import H2O


class SolvatedMonolayer(mb.Compound):
    """Create solvated monolayer system."""
    def __init__(self, monolayer, solvent=H2O(), n_solvents=1000, solvent_box_height=5, seed=12345):
        super(SolvatedMonolayer, self).__init__()
        monolayer_box_lengths = monolayer.get_boundingbox().lengths
        solvent_box = [monolayer_box_lengths[0],
                       monolayer_box_lengths[1],
                       solvent_box_height]
        box_of_solvent = mb.fill_box(compound=solvent,
                                     box=solvent_box,
                                     n_compounds=n_solvents)
        box_of_solvent.translate([0, 0, monolayer_box_lengths[2]])
        self.add(monolayer, label="monolayer")
        self.add(box_of_solvent, label="solvent")


class SolvatedDualMonolayer(mb.Compound):
    def __init__(self, dual_monolayer, solvent=H2O(), n_solvents=1000, seed=12345):
        super(SolvatedDualMonolayer, self).__init__()
        top_monolayer = dual_monolayer["top_monolayer"]
        top_monolayer_box_lengths = top_monolayer.get_boundingbox().lengths
        bottom_monolayer = dual_monolayer["bottom_monolayer"]
        bottom_monolayer_box_lengths = bottom_monolayer.get_boundingbox().lengths
        dual_monolayer_box_lengths = dual_monolayer.get_boundingbox().lengths

        separation = dual_monolayer_box_lengths[2] - (top_monolayer_box_lengths[2] + bottom_monolayer_box_lengths[2])
        solvent_box = [bottom_monolayer_box_lengths[0],
                       bottom_monolayer_box_lengths[1],
                       separation]
        box_of_solvent = mb.fill_box(compound=solvent,
                                     box=solvent_box,
                                     n_compounds=n_solvents)
        box_of_solvent.translate([0, 0, bottom_monolayer_box_lengths[2]])
        self.add(dual_monolayer, label="monolayers")
        self.add(box_of_solvent, label="solvents")
