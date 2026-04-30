import unittest
from datetime import datetime
from clinica import ClinicaVeterinaria

class TestMascota(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Test")
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")

    # ✔ OK
    def test_registrar_mascota_ok(self):
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)

        self.assertEqual(1, len(self.clinica._mascotas))
        m = self.clinica._mascotas[0]

        self.assertEqual("Mambo", m.get_nombre())
        self.assertEqual("Perro", m._especie)
        self.assertEqual(5, m._edad)
        self.assertEqual("Labrador", m.get_raza())
        self.assertEqual(47111111, m.get_dueno().get_dni())

    # ❌ dueño inexistente
    def test_registrar_mascota_dueno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 99999999)

    # ❌ nombre vacío
    def test_registrar_mascota_nombre_vacio(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_mascota("", "Perro", 5, "Labrador", 47111111)

    # ❌ nombre numérico
    def test_registrar_mascota_nombre_numerico(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_mascota("123", "Perro", 5, "Labrador", 47111111)

    # ❌ especie vacía
    def test_registrar_mascota_especie_vacia(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_mascota("Mambo", "", 5, "Labrador", 47111111)

    # ❌ raza vacía
    def test_registrar_mascota_raza_vacia(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_mascota("Mambo", "Perro", 5, "", 47111111)

    # ❌ edad negativa
    def test_registrar_mascota_edad_negativa(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_mascota("Mambo", "Perro", -1, "Labrador", 47111111)

    # ❌ DNI inválido
    def test_registrar_mascota_dni_invalido(self):
        with self.assertRaises(ValueError):
            self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 123)

    # ❌ duplicada (mismo nombre y dueño)
    def test_registrar_mascota_duplicada(self):
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)

        with self.assertRaises(ValueError):
            self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)

    # ✔ eliminar OK
    def test_eliminar_mascota_ok(self):
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)

        self.clinica.eliminar_mascota("Mambo", 47111111)

        self.assertEqual(0, len(self.clinica._mascotas))

    # ❌ eliminar inexistente
    def test_eliminar_mascota_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.eliminar_mascota("NoExiste", 47111111)

    # ❌ eliminar con dueño inexistente
    def test_eliminar_mascota_dueno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.eliminar_mascota("Mambo", 99999999)

    # ❌ eliminar con turno asociado
    def test_eliminar_mascota_con_turno(self):
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")
        self.clinica.registrar_consultorio(1, "Consultorio 1")

        fecha = datetime(2030, 5, 10, 10, 0)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        with self.assertRaises(ValueError):
            self.clinica.eliminar_mascota("Mambo", 47111111)

    # ✔ modificar OK
    def test_modificar_mascota_ok(self):
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)

        self.clinica.modificar_mascota("Mambo", 47111111, 10)

        m = self.clinica._mascotas[0]
        self.assertEqual(10, m._edad)

    # ❌ modificar inexistente
    def test_modificar_mascota_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.modificar_mascota("NoExiste", 47111111, 10)

    # ❌ modificar con dueño inexistente
    def test_modificar_mascota_dueno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.modificar_mascota("Mambo", 99999999, 10)

    # ❌ edad inválida en modificación
    def test_modificar_mascota_edad_invalida(self):
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)

        with self.assertRaises(ValueError):
            self.clinica.modificar_mascota("Mambo", 47111111, -1)