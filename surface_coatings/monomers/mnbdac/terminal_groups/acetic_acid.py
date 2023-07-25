"""AceticAcid terminal group class."""
import mbuild as mb


class AceticAcid(mb.Compound):
    """AceticAcid terminal group class."""

    def __init__(self):
        super().__init__()
        mb.load(
            "acetic_acid.mol2",
            compound=self,
            backend="gmso",
            relative_to_module=self.__module__,
            infer_hierarchy=False,
        )

        self.remove(self[5])
        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[1]")
