import mbuild as mb


class Propanol(mb.Compound):
    def __init__(self):
        super().__init__()
        mb.load("propanol.mol2",
                compound=self,
                backend="gmso",
                relative_to_module=self.__module__,
                infer_hierarchy=False)

        to_remove = [self[4], self[11]]
        for part in to_remove:
            self.remove(part)

        self.labels["side"] = self["Compound[0]"].labels.pop("port[3]")
        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[1]")

