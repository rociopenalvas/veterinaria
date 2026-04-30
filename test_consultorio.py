import unittest
from datetime import datetime
from clinica import ClinicaVeterinaria

class TestConsultorio(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Test")

    # ✔ OK
    def test_registrar_consultorio_ok(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        self.assertEqual(1, len(self.clinica._consultorios))
        c = self.clinica._consultorios[0]

        self.assertEqual(1, c.get_numero())
        self.assertEqual("Consultorio 1", c.get_descripcion())

    # ❌ número string
    def test_registrar_consultorio_numero_string(self):
        with self.assertRaises(TypeError):
            self.clinica.registrar_consultorio("uno", "Consultorio")

    # ❌ número inválido (<= 0)
    def test_registrar_consultorio_numero_invalido(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_consultorio(0, "Consultorio")

    # ❌ descripción vacía
    def test_registrar_consultorio_descripcion_vacia(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_consultorio(1, "")

    # ❌ duplicado
    def test_registrar_consultorio_duplicado(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        with self.assertRaises(ValueError):
            self.clinica.registrar_consultorio(1, "Otro")

    # ✔ eliminar OK
    def test_eliminar_consultorio_ok(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        self.clinica.eliminar_consultorio(1)

        self.assertEqual(0, len(self.clinica._consultorios))

    # ❌ eliminar inexistente
    def test_eliminar_consultorio_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.eliminar_consultorio(99)

    # ❌ eliminar con turno
    def test_eliminar_consultorio_con_turno(self):
        # setup completo
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        fecha = datetime(2030, 5, 10, 10, 0)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        with self.assertRaises(ValueError):
            self.clinica.eliminar_consultorio(1)

    # ✔ modificar OK
    def test_modificar_consultorio_ok(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        self.clinica.modificar_consultorio(1, "Nuevo")

        c = self.clinica._consultorios[0]
        self.assertEqual("Nuevo", c.get_descripcion())

    # ❌ modificar inexistente
    def test_modificar_consultorio_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.modificar_consultorio(99, "Nuevo")

    # ❌ descripción inválida
    def test_modificar_consultorio_descripcion_vacia(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        with self.assertRaises(ValueError):
            self.clinica.modificar_consultorio(1, "")