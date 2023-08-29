"""Routine to create carve crystaline silica interface."""
import mbuild as mb
from mbuild.lib.surfaces import Betacristobalite


class SilicaInterface(mb.Compound):
    """A recipe for creating a crystaline silica interface.

    Parameters
    ----------
    dimensions : tuple of len 2, optional, default=(5.388800 * 1.2, 4.589110 * 1.25)
        Define the x and y dimension of the silica interface.
        Currently not used, pending https://github.com/mosdef-hub/mbuild/pull/1124.
    tile_x : int, optional, default=1
        Option to expand in x dimension by tile_x
    tile_y : int, optional, default=1
        Option to expand in y dimension by tile_y
    """

    def __init__(
        self, dimensions=(5.388800 * 1.2, 4.589110 * 1.25), tile_x=1, tile_y=1
    ):
        super(SilicaInterface, self).__init__()
        # silica_crystal = Betacristobalite(dimensions)
        silica_crystal = Betacristobalite()
        tiled_compound = mb.lib.recipes.TiledCompound(
            mb.clone(silica_crystal), n_tiles=(tile_x, tile_y, 1)
        )
        self.add(tiled_compound, "TiledCompound")
        self._transfer_ports()
        self.periodicity = (True, True, False)

    def _transfer_ports(self):
        """Transfer available ports from TiledCompound to parents level."""
        for port in self["TiledCompound"].available_ports():
            clone_port = mb.clone(port)
            clone_port.anchor = port.anchor
            self.remove(port)
            self.add(clone_port)
