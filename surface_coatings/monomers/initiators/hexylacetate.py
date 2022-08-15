import numpy as np

import mbuild as mb

# HexylAcetate initiator for pMPC
class HexylAcetate(mb.Compound):
    def __init__(self):
        super(HexylAcetate, self).__init__()

        # Look for data file in same directory as this python module.
        mb.load('hexylacetate.pdb', compound=self, relative_to_module=self.__module__)

        # Add "up" port (facing the MPC monomer)
        port_up = mb.Port(anchor=self[0], orientation=[0, -1, 0], separation=0.07)
        self.add(port_up, "up")

        # Add "down" port (facing the Silane group)
        port_down = mb.Port(anchor=self[21], orientation=[0, 1, 0], separation=0.07)
        self.add(port_down , "down")

if __name__ == "__main__":
    ini = HexylAcetate()
    print(ini)
