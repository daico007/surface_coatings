import mbuild as mb

from surface_coatings.surfaces import (
    SilicaInterface,
    SilicaInterfaceCarve,
    SiliconInterface,
    GrapheneSheet,
    AuLattice,

)


class TestSystem(object):
    def test_silicon_interface(self):
        silicon_surface = SiliconInterface(x=10, y=10, z=2)
        assert silicon_surface.periodicity == (True, True, False)

    def test_silica_interface_carve(self):
        silica_surface_carve = SilicaInterfaceCarve()
        assert silica_surface_carve.periodicity == (True, True, False)

    def test_silica_interface(self):
        silica_surface = SilicaInterface()
        assert silica_surface.periodicity == (True, True, False)

    def test_graphene_interface(self):
        graphene_sheet = GrapheneSheet()
        assert graphene_sheet.periodicity == (True, True, False)

    def test_au_interface(self):
        au_interface = AuLattice()
        assert au_interface.periodicity == (True, True, False)