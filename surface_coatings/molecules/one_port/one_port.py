"""Routine to create different terminal group with one connection point/port."""
import mbuild as mb


class OnePort(mb.Compound):
    """A methyl group."""

    def __init__(self, molecule="methyl"):
        super(OnePort, self).__init__()

        mb.load(
            f"./pdbs/{molecule}.pdb",
            compound=self,
            relative_to_module=self.__module__,
        )
        self.translate(-self[0].pos)

        self.add(
            mb.Port(anchor=self[0], orientation=[0, -1, 0], separation=0.07),
            "down",
        )
