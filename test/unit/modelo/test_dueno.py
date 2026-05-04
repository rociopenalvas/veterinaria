import unittest
from clinica import ClinicaVeterinaria


class TestDueno(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Test")

    def test_registrar_dueno_ok(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle 123")

        self.assertEqual(1, len(self.clinica._duenos))
        d = self.clinica._duenos[0]

        self.assertEqual(47111111, d.get_dni())
        self.assertEqual("Soledad", d.get_nombre())
        self.assertEqual("01136111111", d.get_telefono())
        self.assertEqual("Calle 123", d.get_direccion())

    def test_registrar_dueno_dni_string(self):
        with self.assertRaises(TypeError):
            self.clinica.registrar_dueno("abc", "Soledad", "01136111111", "Calle")

    def test_registrar_dueno_dni_invalido(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_dueno(123, "Soledad", "01136111111", "Calle")

    def test_registrar_dueno_nombre_vacio(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_dueno(47111111, "", "01136111111", "Calle")

    def test_registrar_dueno_nombre_numerico(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_dueno(47111111, "1234", "01136111111", "Calle")

    def test_registrar_dueno_telefono_string(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_dueno(47111111, "Soledad", "abc", "Calle")

    def test_registrar_dueno_telefono_corto(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_dueno(47111111, "Soledad", "123", "Calle")

    def test_registrar_dueno_direccion_vacia(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "")

    def test_registrar_dueno_duplicado(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")

        with self.assertRaises(ValueError):
            self.clinica.registrar_dueno(47111111, "Otra", "01136111111", "Calle")

    def test_eliminar_dueno_ok(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")

        self.clinica.eliminar_dueno(47111111)

        self.assertEqual(0, len(self.clinica._duenos))

    def test_eliminar_dueno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.eliminar_dueno(99999999)

    def test_eliminar_dueno_con_mascota(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)

        with self.assertRaises(ValueError):
            self.clinica.eliminar_dueno(47111111)

    def test_modificar_dueno_ok(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")

        self.clinica.modificar_dueno(47111111, "01199999999", "Nueva")

        d = self.clinica._duenos[0]
        self.assertEqual("01199999999", d.get_telefono())
        self.assertEqual("Nueva", d.get_direccion())

    def test_modificar_dueno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.modificar_dueno(99999999, "011", "Dir")

    def test_modificar_dueno_telefono_invalido(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")

        with self.assertRaises(ValueError):
            self.clinica.modificar_dueno(47111111, "abc", "Dir")

    def test_modificar_dueno_direccion_vacia(self):
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")

        with self.assertRaises(ValueError):
            self.clinica.modificar_dueno(47111111, "01199999999", "")
