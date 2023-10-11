"""Toluene terminal group class."""
import mbuild as mb


class Aniline(mb.Compound):
    """Aniline terminal group class."""

    def __init__(self):
        super().__init__()
        mb.load(
            "aniline.mol2",
            compound=self,
            backend="gmso",
            relative_to_module=self.__module__,
            infer_hierarchy=False,
        )

        self.remove(self[12])
        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[1]")
