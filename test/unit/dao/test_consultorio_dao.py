import unittest
from clinica import ClinicaVeterinaria
from dao.consultorio_dao import ConsultorioDAO


class TestConsultorioDAO(unittest.TestCase):

    def test_guardar_y_cargar_consultorios(self):
        clinica = ClinicaVeterinaria("Test")

        clinica.registrar_consultorio(1, "Consultorio 1")

        dao = ConsultorioDAO()

        dao.guardar(clinica._consultorios, "test_data/consultorios.json")

        nueva = ClinicaVeterinaria("Nueva")
        dao.cargar("test_data/consultorios.json", nueva)

        self.assertEqual(1, len(nueva._consultorios))

        c = nueva._consultorios[0]

        self.assertEqual(1, c.get_numero())
        self.assertEqual("Consultorio 1", c.get_descripcion())
