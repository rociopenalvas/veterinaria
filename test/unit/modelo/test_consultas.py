import unittest
from datetime import datetime, date
from clinica import ClinicaVeterinaria


class TestConsultas(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Test")

        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_dueno(47222222, "Juan", "01122222222", "Otra")

        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        self.clinica.registrar_mascota("Luna", "Gato", 3, "Siames", 47222222)

        self.clinica.registrar_veterinario(
            87654321, "Dr1", "10987654321", "MAT1", "General"
        )
        self.clinica.registrar_veterinario(
            12345678, "Dr2", "10123456789", "MAT2", "Cirugia"
        )

        self.clinica.registrar_consultorio(1, "C1")
        self.clinica.registrar_consultorio(2, "C2")

        self.fecha1 = datetime(2032, 12, 12, 10, 0)
        self.fecha2 = datetime(2032, 12, 13, 10, 0)
        self.fecha3 = datetime(2032, 12, 12, 11, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, self.fecha1)
        self.clinica.agendar_turno("Luna", 47222222, "MAT2", 2, self.fecha2)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT2", 2, self.fecha3)

    def test_turnos_por_fecha_filtra_correcto(self):
        res = self.clinica.turnos_por_fecha(self.fecha1.date())

        self.assertEqual(2, len(res))

        nombres = [t.get_mascota().get_nombre() for t in res]
        self.assertIn("Mambo", nombres)

    def test_turnos_por_fecha_sin_resultados(self):
        res = self.clinica.turnos_por_fecha(date(2035, 1, 1))
        self.assertEqual(0, len(res))

    def test_turnos_por_veterinario_filtra(self):
        res = self.clinica.turnos_por_veterinario("MAT2")

        self.assertEqual(2, len(res))

        for t in res:
            self.assertEqual("MAT2", t.get_veterinario().get_matricula())

    def test_turnos_por_veterinario_inexistente(self):
        res = self.clinica.turnos_por_veterinario("NO")
        self.assertEqual(0, len(res))

    def test_turnos_por_mascota_filtra(self):
        res = self.clinica.turnos_por_mascota("Mambo", 47111111)

        self.assertEqual(2, len(res))

        for t in res:
            self.assertEqual("Mambo", t.get_mascota().get_nombre())

    def test_turnos_por_mascota_inexistente(self):
        res = self.clinica.turnos_por_mascota("NoExiste", 47111111)
        self.assertEqual(0, len(res))

    def test_turnos_por_dueno_filtra(self):
        res = self.clinica.turnos_por_dueno(47111111)

        self.assertEqual(2, len(res))

        for t in res:
            self.assertEqual(47111111, t.get_mascota().get_dueno().get_dni())

    def test_turnos_por_dueno_inexistente(self):
        res = self.clinica.turnos_por_dueno(99999999)
        self.assertEqual(0, len(res))

    def test_turnos_cancelados_no_aparecen(self):
        turno_id = self.clinica._turnos[0].get_id()
        self.clinica.cancelar_turno(turno_id)

        res = self.clinica.turnos_por_dueno(47111111)

        self.assertEqual(1, len(res))
