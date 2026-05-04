import unittest
from clinica import ClinicaVeterinaria
from dao.dueno_dao import DuenoDAO
from dao.mascota_dao import MascotaDAO


class TestMascotaDAO(unittest.TestCase):

    def test_guardar_y_cargar_mascotas(self):
        clinica = ClinicaVeterinaria("Test")

        clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)

        dao_dueno = DuenoDAO()
        dao_mascota = MascotaDAO()

        dao_dueno.guardar(clinica._duenos, "test_data/duenos.json")
        dao_mascota.guardar(clinica._mascotas, "test_data/mascotas.json")

        nueva = ClinicaVeterinaria("Nueva")

        dao_dueno.cargar("test_data/duenos.json", nueva)
        dao_mascota.cargar("test_data/mascotas.json", nueva)

        self.assertEqual(1, len(nueva._mascotas))

        m = nueva._mascotas[0]

        self.assertEqual("Mambo", m.get_nombre())
        self.assertEqual("Perro", m._especie)
        self.assertEqual(5, m._edad)
        self.assertEqual("Labrador", m.get_raza())
        self.assertEqual(47111111, m.get_dueno().get_dni())
