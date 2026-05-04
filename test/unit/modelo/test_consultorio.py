import unittest
from datetime import datetime
from clinica import ClinicaVeterinaria


class TestConsultorio(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Test")

    def test_registrar_consultorio_ok(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        self.assertEqual(1, len(self.clinica._consultorios))
        c = self.clinica._consultorios[0]

        self.assertEqual(1, c.get_numero())
        self.assertEqual("Consultorio 1", c.get_descripcion())

    def test_registrar_consultorio_numero_string(self):
        with self.assertRaises(TypeError):
            self.clinica.registrar_consultorio("uno", "Consultorio")

    def test_registrar_consultorio_numero_invalido(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_consultorio(0, "Consultorio")

    def test_registrar_consultorio_descripcion_vacia(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_consultorio(1, "")

    def test_registrar_consultorio_duplicado(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        with self.assertRaises(ValueError):
            self.clinica.registrar_consultorio(1, "Otro")

    def test_eliminar_consultorio_ok(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        self.clinica.eliminar_consultorio(1)

        self.assertEqual(0, len(self.clinica._consultorios))

    def test_eliminar_consultorio_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.eliminar_consultorio(99)

    def test_eliminar_consultorio_con_turno(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        self.clinica.registrar_veterinario(
            87654321, "Dr", "10987654321", "MAT1", "General"
        )
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        fecha = datetime(2030, 5, 10, 10, 0)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        with self.assertRaises(ValueError):
            self.clinica.eliminar_consultorio(1)

    def test_eliminar_consultorio_con_turno_cancelado(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        self.clinica.registrar_veterinario(
            87654321, "Dr", "10987654321", "MAT1", "General"
        )
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        fecha = datetime(2030, 5, 10, 10, 0)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)
        turno_id = self.clinica._turnos[0].get_id()
        self.clinica.cancelar_turno(turno_id)

        self.clinica.eliminar_consultorio(1)
        self.assertEqual(0, len(self.clinica._consultorios))

    def test_eliminar_consultorio_con_turno_activo_pasado(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        self.clinica.registrar_veterinario(
            87654321, "Dr", "10987654321", "MAT1", "General"
        )
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        self.clinica.restaurar_turno(
            "Mambo", 47111111, "MAT1", 1, datetime(2025, 5, 10, 10, 0), 70, "Activo"
        )

        self.clinica.eliminar_consultorio(1)
        self.assertEqual(0, len(self.clinica._consultorios))

    def test_modificar_consultorio_ok(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        self.clinica.modificar_consultorio(1, "Nuevo")

        c = self.clinica._consultorios[0]
        self.assertEqual("Nuevo", c.get_descripcion())

    def test_modificar_consultorio_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.modificar_consultorio(99, "Nuevo")

    def test_modificar_consultorio_descripcion_vacia(self):
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        with self.assertRaises(ValueError):
            self.clinica.modificar_consultorio(1, "")
