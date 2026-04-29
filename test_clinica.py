import unittest
from datetime import datetime, timedelta, date
from clinica import ClinicaVeterinaria


class TestClinica(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Clinica Test")

        # Datos base
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle 123")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")
        self.clinica.registrar_consultorio(1, "Consultorio 1")

    def test_registrar_dueno(self):
        self.assertEqual(1, len(self.clinica._duenos))
        dueno = self.clinica._duenos[0]

        self.assertEqual(47111111, dueno.get_dni())
        self.assertEqual("Soledad", dueno.get_nombre())
        self.assertEqual("01136111111", dueno.get_telefono())
        self.assertEqual("Calle 123", dueno.get_direccion())

    def test_registrar_mascota(self):
        self.assertEqual(1, len(self.clinica._mascotas))
        mascota = self.clinica._mascotas[0]

        self.assertEqual("Mambo", mascota.get_nombre())
        self.assertEqual("Perro", mascota._especie)
        self.assertEqual(5, mascota._edad)
        self.assertEqual("Labrador", mascota.get_raza())
        self.assertEqual(47111111, mascota.get_dueno().get_dni())

    def test_registrar_veterinario(self):
        self.assertEqual(1, len(self.clinica._veterinarios))
        vet = self.clinica._veterinarios[0]

        self.assertEqual(87654321, vet.get_dni())
        self.assertEqual("Dr", vet.get_nombre())
        self.assertEqual("10987654321", vet.get_telefono())
        self.assertEqual("MAT1", vet.get_matricula())
        self.assertEqual("General", vet.get_especialidad())

    def test_agendar_turno(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno(
            "Mambo", 47111111, "MAT1", 1, fecha
        )

        self.assertEqual(1, len(self.clinica._turnos))

        turno = self.clinica._turnos[0]
        self.assertEqual("Activo", turno.get_estado())
        self.assertEqual("Mambo", turno.get_mascota().get_nombre())
        self.assertEqual("MAT1", turno.get_veterinario().get_matricula())

    def test_turno_superpuesto(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno(
            "Mambo", 47111111, "MAT1", 1, fecha
        )

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno(
                "Mambo", 47111111, "MAT1", 1, fecha
            )

    def test_cancelar_turno(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno(
            "Mambo", 47111111, "MAT1", 1, fecha
        )

        turno_id = self.clinica._turnos[0].get_id()

        self.clinica.cancelar_turno(turno_id)

        self.assertEqual("Cancelado", self.clinica._turnos[0].get_estado())

    # 🔽 NUEVOS TESTS

    def test_modificar_turno(self):
        fecha = datetime(2032, 12, 12, 10, 0)
        nueva_fecha = datetime(2032, 12, 10, 10, 0)

        self.clinica.agendar_turno(
            "Mambo", 47111111, "MAT1", 1, fecha
        )

        turno_id = self.clinica._turnos[0].get_id()

        self.clinica.modificar_turno(turno_id, nueva_fecha)

        self.assertEqual(
            nueva_fecha,
            self.clinica._turnos[0].get_fecha_hora()
        )

    def test_turnos_por_fecha(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno(
            "Mambo", 47111111, "MAT1", 1, fecha
        )

        resultados = self.clinica.turnos_por_fecha(fecha.date())

        self.assertEqual(1, len(resultados))
        self.assertEqual("Mambo", resultados[0].get_mascota().get_nombre())

    def test_turnos_por_veterinario(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno(
            "Mambo", 47111111, "MAT1", 1, fecha
        )

        resultados = self.clinica.turnos_por_veterinario("MAT1")

        self.assertEqual(1, len(resultados))
        self.assertEqual("MAT1", resultados[0].get_veterinario().get_matricula())

    def test_turno_fecha_pasada(self):
        fecha_pasada = datetime(2020, 1, 1, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno(
                "Mambo", 47111111, "MAT1", 1, fecha_pasada
            )

    def test_mascota_inexistente(self):
        fecha = datetime(2030, 5, 10, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno(
                "NoExiste", 47111111, "MAT1", 1, fecha
            )
 
    def test_veterinario_inexistente(self):
        fecha = datetime(2030, 5, 10, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno(
                "Mambo", 47111111, "MAT999", 1, fecha
            )

    def test_consultorio_ocupado(self):
        fecha = datetime(2030, 5, 10, 10, 0)

        self.clinica.agendar_turno(
            "Mambo", 47111111, "MAT1", 1, fecha
        )

        # mismo consultorio y horario → error
        with self.assertRaises(ValueError):
            self.clinica.agendar_turno(
                "Mambo", 47111111, "MAT1", 1, fecha
            )

    def test_eliminar_mascota_con_turno(self):
        fecha = datetime(2030, 5, 10, 10, 0)

        self.clinica.agendar_turno(
            "Mambo", 47111111, "MAT1", 1, fecha
        )

        with self.assertRaises(ValueError):
            self.clinica.eliminar_mascota("Mambo", 47111111)

    def test_modificar_mascota(self):
        self.clinica.modificar_mascota("Mambo", 47111111, 10)

        mascota = self.clinica._mascotas[0]
        self.assertEqual(10, mascota._edad)
        
if __name__ == "__main__":
    unittest.main()