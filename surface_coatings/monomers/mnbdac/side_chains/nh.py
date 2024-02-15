"""A NH with 2 ports."""

import numpy as np

import mbuild as mb


class NH(mb.Compound):
    """A NH with 2 ports."""

    def __init__(self):
        super().__init__()

        self.add(mb.load("N", smiles=True))

        h_to_remove = [self[2], self[3]]
        for h in h_to_remove:
            self.remove(h)

        self.labels["side"] = self["Compound[0]"].labels.pop("port[1]")
        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[3]")
