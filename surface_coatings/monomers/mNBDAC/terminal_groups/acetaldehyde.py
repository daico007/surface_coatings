import mbuild as mb 

class Acetaldehyde(mb.Compound):
    def __init__(self):
        super().__init__()
        mb.load("acetaldehyde.mol2",
                 compound=self,
                 backend="gmso",
                 relative_to_module=self.__module__)
        self.remove(self[4])
        self.labels["terminal"] = self["Compound[0]"].labels.pop("port[1]")
        
