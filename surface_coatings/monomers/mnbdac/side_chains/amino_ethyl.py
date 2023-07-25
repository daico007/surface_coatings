"""AminoEthyl side chain class."""
import mbuild as mb


class AminoEthyl(mb.Compound):
    """AminoEthyl side chain class."""

    def __init__(self):
        super().__init__()
        mb.load(
            "amino_ethane.mol2",
            compound=self,
            backend="gmso",
            relative_to_module=self.__module__,
            infer_hierarchy=False,
        )

        to_remove = [self[5], self[9]]
        for part in to_remove:
            self.remove(part)

        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[1]")
        self.labels["side"] = self["Compound[0]"].labels.pop("port[3]")
