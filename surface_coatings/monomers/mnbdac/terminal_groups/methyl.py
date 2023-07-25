"""Methyl terminal group class."""
import mbuild as mb


class Methyl(mb.Compound):
    """Methyl terminal group class."""

    def __init__(self):
        super().__init__()
        mb.load(
            "methane.mol2",
            compound=self,
            backend="gmso",
            relative_to_module=self.__module__,
            infer_hierarchy=False,
        )

        self.remove(self[4])
        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[1]")
