import mbuild as mb
from mbuild.lib.surfaces import Betacristobalite

class SilicaInterface(mb.Compound):
    def __init__(self, dimensions=(5.388800 * 1.2, 4.589110 * 1.25), tile_x=1, tile_y=1):
        super(SilicaInterface, self).__init__()
        silica_crystal = Betacristobalite(dimensions)
        tiled_compound = mb.lib.recipes.TiledCompound(mb.clone(silica_crystal),
                                                      n_tiles=(tile_x, tile_y, 1))
        self.add(tiled_compound, "TiledCompound")
        self._transfer_ports()
        self.periodicity = (True, True, False)

    def _transfer_ports(self):
        """Transfer available ports from TiledCompound to parents level"""
        for port in self["TiledCompound"].available_ports():
            clone_port = mb.clone(port)
            clone_port.anchor = port.anchor
            self.remove(port)
            self.add(clone_port)