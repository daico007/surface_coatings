"""AminoMethyl side chain class."""
import mbuild as mb


class AminoMethyl(mb.Compound):
    """AminoEthyl side chain class."""

    def __init__(self):
        super().__init__()
        mb.load(
            "amino_methane.mol2",
            compound=self,
            backend="gmso",
            relative_to_module=self.__module__,
            infer_hierarchy=False,
        )

        to_remove = [self[4], self[6]]
        for part in to_remove:
            self.remove(part)

        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[1]")
        self.labels["side"] = self["Compound[0]"].labels.pop("port[3]")
