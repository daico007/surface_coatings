import mbuild as mb
from mbuild.lib.atoms import H
from mbuild.lib.moieties import CH2, CH3

class SBMA(mb.Compound):
    def __init__(self, front_cap=False, rear_cap=False):
        super(SBMA, self).__init__()
        self.add(mb.load('CC(=C)C(=O)OCC[N+](C)(C)CCCS([O-])(=O)=O', smiles=True))
        self.translate(-self[1].pos)
        bond_vect = self[1].pos - self[2].pos
        self.add(mb.Port(anchor=self[1], orientation=bond_vect, separation=0.07), 'up')
        self.add(mb.Port(anchor=self[2], orientation=bond_vect, separation=-0.07), 'down')
        if front_cap: 
            hydrogen = H() 
            # call forceoverlap
        if rear_cap:
            hydrogen = H()
            # call forceoverlap