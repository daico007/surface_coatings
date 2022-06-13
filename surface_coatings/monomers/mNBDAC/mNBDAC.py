import mbuild as mb 

# Backbone monomer
class mNBDAC(mb.Compound):
    def __init__(self):
        super().__init__()
        self.add(mb.load("C=CC1C(C(=O)Cl)C(C(=O)Cl)C(C=C)C1", smiles=True))
        self.name = "mNBDAC"

        c_to_remove = [self[0], self[13]]
        h_to_remove = [self[15], self[16], self[23], self[24]]
        cl_to_remove = [self[6], self[10]]

        for c in c_to_remove:
            self.remove(c)
        for h in h_to_remove:
            self.remove(h)
        
        self.labels["up"] = self["Compound[0]"].labels.pop("port[1]")
        self.labels["down"] = self["Compound[0]"].labels.pop("port[7]")
        
         
        for cl in cl_to_remove:
            self.remove(cl)
        self.labels['side0'] = self["Compound[0]"].labels.pop("port[13]")
        self.labels['side1'] = self["Compound[0]"].labels.pop("port[15]")
