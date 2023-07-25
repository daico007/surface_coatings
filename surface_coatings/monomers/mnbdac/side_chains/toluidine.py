"""Toluidine side chain class."""
import mbuild as mb


class Toluidine(mb.Compound):
    """Toluidine side chain class."""

    def __init__(self):
        super().__init__()
        mb.load(
            "toluidine.mol2",
            compound=self,
            backend="gmso",
            relative_to_module=self.__module__,
            infer_hierarchy=False,
        )

        to_remove = [self[8], self[15]]
        for part in to_remove:
            self.remove(part)

        self.labels["side"] = self["Compound[0]"].labels.pop("port[1]")
        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[3]")
