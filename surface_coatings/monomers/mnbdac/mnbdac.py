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
        
        up_port = self["Compound[0]"].labels.pop("port[1]")
        down_port = self["Compound[0]"].labels.pop("port[7]")

        up_port.referrers.add(self)
        down_port.referrers.add(self)
        self.labels["up"] = up_port
        self.labels["down"] = down_port

        for cl in cl_to_remove:
            self.remove(cl)

        side0_port = self["Compound[0]"].labels.pop("port[13]")
        side1_port = self["Compound[0]"].labels.pop("port[15]")

        side0_port.referrers.add(self)
        side1_port.referrers.add(self)
        self.labels['side0'] = side0_port
        self.labels['side1'] = side1_port
