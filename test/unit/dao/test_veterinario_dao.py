import unittest
from clinica import ClinicaVeterinaria
from dao.veterinario_dao import VeterinarioDAO


class TestVeterinarioDAO(unittest.TestCase):

    def test_guardar_y_cargar_veterinarios(self):
        clinica = ClinicaVeterinaria("Test")

        clinica.registrar_veterinario(
            87654321, "Dr", "10987654321", "MAT1", "General"
        )

        dao = VeterinarioDAO()

        dao.guardar(clinica._veterinarios, "test_data/veterinarios.json")

        nueva = ClinicaVeterinaria("Nueva")
        dao.cargar("test_data/veterinarios.json", nueva)

        self.assertEqual(1, len(nueva._veterinarios))

        v = nueva._veterinarios[0]

        self.assertEqual(87654321, v.get_dni())
        self.assertEqual("Dr", v.get_nombre())
        self.assertEqual("10987654321", v.get_telefono())
        self.assertEqual("MAT1", v.get_matricula())
        self.assertEqual("General", v.get_especialidad())
