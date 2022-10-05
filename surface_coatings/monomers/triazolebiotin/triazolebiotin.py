import mbuild as mb
from mbuild.lib.atoms import H
from mbuild.lib.moieties import CH2, CH3

class TriazoleBiotin(mb.Compound):
    def __init__(self, front_cap=False, rear_cap=False):
        super(TriazoleBiotin, self).__init__()
        #self.add(mb.load('C(=C)C(=O)OCCCN1C=C(N=N1)CCCCCC2C3C(CS2)NC(=O)N3', smiles=True))
        mb.load("triazolebiotin.mol2", 
                compound=self, 
                relative_to_module=self.__module__, 
                backend="gmso",
                infer_hierarchy=False)
        self.translate(-self[1].pos)

        self.remove(self[27])

        ch3 = CH3()
        self.add(ch3)

        mb.force_overlap(move_this=ch3,
                        from_positions=ch3['up'],
                        to_positions=self['Compound[0]']['port[1]'])

        bond_vect = self[1].pos - self[0].pos

        self.add(mb.Port(anchor=self[0], orientation=bond_vect, separation=-0.07), 'down')
        self.add(mb.Port(anchor=self[1], orientation=bond_vect, separation=0.07), 'up')

        if front_cap:
            hydrogen = H()
            # TODO call force_overlap
        if rear_cap:
            hydrogen = H()
            # TODO call force_overlap

if __name__ == "__main__":
    compound = TriazoleBiotin()
    print(compound)
