import unittest
from datetime import datetime
from clinica import ClinicaVeterinaria


class TestTurno(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Test")

        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)
        self.clinica.registrar_veterinario(
            87654321, "Dr", "10987654321", "MAT1", "General"
        )
        self.clinica.registrar_consultorio(1, "Consultorio 1")

    def test_agendar_turno_ok(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        self.assertEqual(1, len(self.clinica._turnos))
        t = self.clinica._turnos[0]

        self.assertEqual("Activo", t.get_estado())
        self.assertEqual("Mambo", t.get_mascota().get_nombre())
        self.assertEqual("MAT1", t.get_veterinario().get_matricula())

    def test_agendar_turno_fecha_pasada(self):
        fecha = datetime(2020, 1, 1, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

    def test_agendar_turno_mascota_inexistente(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("NoExiste", 47111111, "MAT1", 1, fecha)

    def test_agendar_turno_dueno_inexistente(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 99999999, "MAT1", 1, fecha)

    def test_agendar_turno_veterinario_inexistente(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "NO", 1, fecha)

    def test_agendar_turno_consultorio_inexistente(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 99, fecha)

    def test_turno_superpuesto(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

    def test_turno_mismo_veterinario(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        self.clinica.registrar_mascota("Otro", "Perro", 3, "Lab", 47111111)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Otro", 47111111, "MAT1", 1, fecha)

    def test_turno_mismo_consultorio(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        self.clinica.registrar_veterinario(
            12345678, "Otro", "01111111111", "MAT2", "General"
        )

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "MAT2", 1, fecha)

    def test_agendar_turno_minuto_no_permitido(self):
        fecha = datetime(2032, 12, 12, 10, 10)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

    def test_agendar_turno_minuto_permitido_15(self):
        fecha = datetime(2032, 12, 12, 10, 15)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        self.assertEqual(1, len(self.clinica._turnos))
        self.assertEqual(fecha, self.clinica._turnos[0].get_fecha_hora())

    def test_turno_superpuesto_intervalo_mismo_veterinario(self):
        self.clinica.registrar_consultorio(2, "Consultorio 2")
        self.clinica.registrar_dueno(47222222, "Juan", "01122222222", "Otra")
        self.clinica.registrar_mascota("Luna", "Gato", 3, "Siames", 47222222)

        t0 = datetime(2032, 12, 12, 10, 0)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, t0)

        # Mismo vet: 10:00-10:30 choca con 10:15-10:45.
        t15 = datetime(2032, 12, 12, 10, 15)
        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Luna", 47222222, "MAT1", 2, t15)

    def test_cancelar_turno_ok(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        turno_id = self.clinica._turnos[0].get_id()
        self.clinica.cancelar_turno(turno_id)

        self.assertEqual("Cancelado", self.clinica._turnos[0].get_estado())

    def test_cancelar_turno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.cancelar_turno(999)

    def test_cancelar_turno_dos_veces(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)
        turno_id = self.clinica._turnos[0].get_id()

        self.clinica.cancelar_turno(turno_id)

        with self.assertRaises(ValueError):
            self.clinica.cancelar_turno(turno_id)

    def test_modificar_turno_ok(self):
        fecha = datetime(2032, 12, 12, 10, 0)
        nueva = datetime(2032, 12, 13, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        turno_id = self.clinica._turnos[0].get_id()
        self.clinica.modificar_turno(turno_id, nueva)

        self.assertEqual(nueva, self.clinica._turnos[0].get_fecha_hora())

    def test_modificar_turno_fecha_pasada(self):
        fecha = datetime(2032, 12, 12, 10, 0)
        nueva = datetime(2020, 1, 1, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        turno_id = self.clinica._turnos[0].get_id()

        with self.assertRaises(ValueError):
            self.clinica.modificar_turno(turno_id, nueva)

    def test_modificar_turno_minuto_no_permitido(self):
        fecha = datetime(2032, 12, 12, 10, 0)
        nueva = datetime(2032, 12, 13, 10, 10)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)
        turno_id = self.clinica._turnos[0].get_id()

        with self.assertRaises(ValueError):
            self.clinica.modificar_turno(turno_id, nueva)

    def test_modificar_turno_conflicto_por_intervalo(self):
        self.clinica.registrar_consultorio(2, "Consultorio 2")
        self.clinica.registrar_veterinario(
            12345678, "Otro", "01111111111", "MAT2", "General"
        )

        d10 = datetime(2032, 12, 12, 10, 0)
        d11 = datetime(2032, 12, 12, 11, 0)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, d10)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT2", 2, d11)

        turno_a_modificar = self.clinica._turnos[1].get_id()

        # Misma mascota: mover el 2º a 10:15 pisa el bloque del primero.
        with self.assertRaises(ValueError):
            self.clinica.modificar_turno(
                turno_a_modificar, datetime(2032, 12, 12, 10, 15)
            )

    def test_turnos_pegados_no_se_superponen(self):
        self.clinica.registrar_dueno(47222222, "Juan", "01122222222", "Otra")
        self.clinica.registrar_mascota("Luna", "Gato", 3, "Siames", 47222222)
        self.clinica.registrar_veterinario(
            12345678, "Otro", "01111111111", "MAT2", "General"
        )

        t1030 = datetime(2032, 12, 12, 10, 30)
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, t1030)

        # 11:00 arranca al terminar 10:30: no hay solape (cambian vet, mascota, etc.).
        t1100 = datetime(2032, 12, 12, 11, 0)
        self.clinica.agendar_turno("Luna", 47222222, "MAT2", 1, t1100)

        self.assertEqual(2, len(self.clinica._turnos))

    def test_modificar_turno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.modificar_turno(999, datetime(2032, 12, 13, 10, 0))
