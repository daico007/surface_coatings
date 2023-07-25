"""Hexafluorobenzene terminal group class."""
import mbuild as mb


class Hexafluorobenzene(mb.Compound):
    """Hexafluorobenzene terminal group class."""

    def __init__(self):
        super().__init__()
        mb.load(
            "hexafluorobenzene.mol2",
            compound=self,
            backend="gmso",
            relative_to_module=self.__module__,
            infer_hierarchy=False,
        )

        self.remove(self[7])
        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[1]")
