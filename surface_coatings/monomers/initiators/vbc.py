"""VBC initiator class."""
import mbuild as mb
from mbuild.lib.atoms import H
from mbuild.lib.moieties import CH2, CH3


# VBC initiator (already plugged out Cl)
class VBC(mb.Compound):
    """VBC initiator class."""

    def __init__(self):
        super(VBC, self).__init__()
        # self.add(mb.load('CC1=CC=C(C=C1)C=C', smiles=True))
        mb.load(
            "vbc.mol2",
            compound=self,
            relative_to_module=self.__module__,
            backend="gmso",
            infer_hierarchy=False,
        )
        self.translate(-self[1].pos)
        bond_vect = self[8].pos - self[7].pos
        self.add(
            mb.Port(anchor=self[8], orientation=bond_vect, separation=0.07),
            "up",
        )

        # Need to find the H that need to be removed (port will be added automatically)
        self.remove(self[10])
        for port in self.all_ports():
            if not port.access_labels:
                self.labels["down"] = port


if __name__ == "__main__":
    compound = VBC()
    print(compound)
