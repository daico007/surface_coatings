import mbuild as mb
from mbuild.lib.recipes import Alkane
from mbuild.lib.moieties import Silane

from util.helper.recipes.one_port import Methyl
class Alkylsilane(mb.Compound):
    """A terminal-functionalized alkylsilane chain.

    An alkylsilane chain featuring a user-specified functional group at one
    terminus and a silane group (featuring an open port to attach to a surface)
    at the other terminus.

    Parameters
    ----------
    chain_length : int
        Length of the chain (number of carbons)
    terminal_group : str
       Functional group to attach to the chain terminus. Valid option for this
       repository is `methyl`, but more can be easily added by providing
       appropriate supplement structure files.
    """
    def __init__(self, chain_length, terminal_group):
        super(Alkylsilane, self).__init__()
        terminal_group_dict = {"methyl":Methyl}
        tgroup = terminal_group_dict[terminal_group]()

        alkane = Alkane(chain_length, cap_front=False, cap_end=False)
        self.add(alkane, 'alkane')
        self.add(tgroup, 'terminal_group')
        mb.force_overlap(self['alkane'], self['alkane']['up'],
                         self['terminal_group']['down'])
        silane = Silane()
        self.add(silane, 'silane')
        mb.force_overlap(self['silane'], self['silane']['up'], self['alkane']['down'])

        self.add(silane['down'], 'down', containment=False)
