"""An oxygen with 2 ports."""

import numpy as np

import mbuild as mb


class O(mb.Compound):
    """A oxygen with 2 ports."""

    def __init__(self):
        super().__init__()
        self.add(mb.Particle(name="O", element="O"))

        self.add(mb.Port(anchor=self[0]), "side")
        self["side"].translate(np.array([0, 0.07, 0]))

        self.add(mb.Port(anchor=self[0]), "terminal")
        self["terminal"].translate(np.array([0, -0.07, 0]))
