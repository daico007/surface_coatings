import mbuild as mb
from surface_coatings.surfaces import SiliconInterface, SilicaInterfaceCarve


class TestSystem(object):
    def test_silicon_interface(self):
        silicon_surface = SiliconInterface()
        assert silicon_surface.periodicity == (True, True, False)

    def test_silica_interface_carve(self):
        silica_surface = SilicaInterfaceCarve()
        assert silica_surface.periodicity == (True, True, False)