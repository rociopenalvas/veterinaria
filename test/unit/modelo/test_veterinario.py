import unittest
from datetime import datetime
from clinica import ClinicaVeterinaria


class TestVeterinario(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Test")

    def test_registrar_veterinario_ok(self):
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")

        self.assertEqual(1, len(self.clinica._veterinarios))
        v = self.clinica._veterinarios[0]

        self.assertEqual(87654321, v.get_dni())
        self.assertEqual("Dr", v.get_nombre())
        self.assertEqual("10987654321", v.get_telefono())
        self.assertEqual("MAT1", v.get_matricula())
        self.assertEqual("General", v.get_especialidad())

    def test_registrar_veterinario_dni_string(self):
        with self.assertRaises(TypeError):
            self.clinica.registrar_veterinario("abc", "Dr", "10987654321", "MAT1", "General")

    def test_registrar_veterinario_dni_invalido(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_veterinario(123, "Dr", "10987654321", "MAT1", "General")

    def test_registrar_veterinario_nombre_vacio(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_veterinario(87654321, "", "10987654321", "MAT1", "General")

    def test_registrar_veterinario_nombre_numerico(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_veterinario(87654321, "123", "10987654321", "MAT1", "General")

    def test_registrar_veterinario_telefono_invalido(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_veterinario(87654321, "Dr", "abc", "MAT1", "General")

    def test_registrar_veterinario_telefono_corto(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_veterinario(87654321, "Dr", "123", "MAT1", "General")

    def test_registrar_veterinario_matricula_vacia(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "", "General")

    def test_registrar_veterinario_especialidad_vacia(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "")

    def test_registrar_veterinario_duplicado(self):
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")

        with self.assertRaises(ValueError):
            self.clinica.registrar_veterinario(12345678, "Otro", "10987654366", "MAT1", "General")

    def test_eliminar_veterinario_ok(self):
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")

        self.clinica.eliminar_veterinario("MAT1")

        self.assertEqual(0, len(self.clinica._veterinarios))

    def test_eliminar_veterinario_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.eliminar_veterinario("NOEXISTE")

    def test_eliminar_veterinario_con_turno(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")
        self.clinica.registrar_consultorio(1, "C1")

        fecha = datetime(2030, 5, 10, 10, 0)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        with self.assertRaises(ValueError):
            self.clinica.eliminar_veterinario("MAT1")

    def test_eliminar_veterinario_con_turno_cancelado(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")
        self.clinica.registrar_consultorio(1, "C1")

        fecha = datetime(2030, 5, 10, 10, 0)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)
        turno_id = self.clinica._turnos[0].get_id()
        self.clinica.cancelar_turno(turno_id)

        self.clinica.eliminar_veterinario("MAT1")
        self.assertEqual(0, len(self.clinica._veterinarios))

    def test_eliminar_veterinario_con_turno_activo_pasado(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")
        self.clinica.registrar_consultorio(1, "C1")

        self.clinica.restaurar_turno(
            "Mambo", 47111111, "MAT1", 1, datetime(2025, 5, 10, 10, 0), 60, "Activo"
        )

        self.clinica.eliminar_veterinario("MAT1")
        self.assertEqual(0, len(self.clinica._veterinarios))

    def test_modificar_veterinario_ok(self):
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")

        self.clinica.modificar_veterinario("MAT1", "01199999999", "Cirugia")

        v = self.clinica._veterinarios[0]
        self.assertEqual("01199999999", v.get_telefono())
        self.assertEqual("Cirugia", v.get_especialidad())

    def test_modificar_veterinario_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.modificar_veterinario("NO", "011", "X")

    def test_modificar_veterinario_telefono_invalido(self):
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")

        with self.assertRaises(ValueError):
            self.clinica.modificar_veterinario("MAT1", "abc", "Cirugia")

    def test_modificar_veterinario_especialidad_vacia(self):
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")

        with self.assertRaises(ValueError):
            self.clinica.modificar_veterinario("MAT1", "01199999999", "")
