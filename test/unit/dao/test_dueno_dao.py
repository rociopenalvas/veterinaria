import unittest
from clinica import ClinicaVeterinaria
from dao.dueno_dao import DuenoDAO


class TestDuenoDAO(unittest.TestCase):
    def test_guardar_y_cargar_duenos(self):
        clinica = ClinicaVeterinaria("Test")

        clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")

        dao = DuenoDAO()
        dao.guardar(clinica._duenos, "test_data/duenos.json")

        nueva = ClinicaVeterinaria("Nueva")
        dao.cargar("test_data/duenos.json", nueva)

        d = nueva._duenos[0]

        self.assertEqual(47111111, d.get_dni())
        self.assertEqual("Soledad", d.get_nombre())
        self.assertEqual("01136111111", d.get_telefono())
        self.assertEqual("Calle", d.get_direccion())