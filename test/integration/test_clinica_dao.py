import unittest
from clinica import ClinicaVeterinaria
from dao.clinica_dao import ClinicaDAO


class TestClinicaDAO(unittest.TestCase):

    def test_guardar_y_cargar(self):
        clinica = ClinicaVeterinaria("Test")
        dao = ClinicaDAO()

        clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")

        dao.guardar(clinica, "test_data/")

        nueva = ClinicaVeterinaria("Nueva")
        dao.cargar(nueva, "test_data/")

        self.assertEqual(len(clinica._duenos), len(nueva._duenos))


