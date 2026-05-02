import unittest
from datetime import datetime
from clinica import ClinicaVeterinaria


class TestTurno(unittest.TestCase):

    def setUp(self):
        self.clinica = ClinicaVeterinaria("Test")

        # base completa
        self.clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        self.clinica.registrar_mascota("Mambo", "Perro", 5, "Labrador", 47111111)
        self.clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")
        self.clinica.registrar_consultorio(1, "Consultorio 1")

    # ✔ OK
    def test_agendar_turno_ok(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        self.assertEqual(1, len(self.clinica._turnos))
        t = self.clinica._turnos[0]

        self.assertEqual("Activo", t.get_estado())
        self.assertEqual("Mambo", t.get_mascota().get_nombre())
        self.assertEqual("MAT1", t.get_veterinario().get_matricula())

    # ❌ fecha pasada
    def test_agendar_turno_fecha_pasada(self):
        fecha = datetime(2020, 1, 1, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

    # ❌ mascota inexistente
    def test_agendar_turno_mascota_inexistente(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("NoExiste", 47111111, "MAT1", 1, fecha)

    # ❌ dueño inexistente
    def test_agendar_turno_dueno_inexistente(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 99999999, "MAT1", 1, fecha)

    # ❌ veterinario inexistente
    def test_agendar_turno_veterinario_inexistente(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "NO", 1, fecha)

    # ❌ consultorio inexistente
    def test_agendar_turno_consultorio_inexistente(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 99, fecha)

    # ❌ superposición mismo todo
    def test_turno_superpuesto(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

    # ❌ mismo veterinario
    def test_turno_mismo_veterinario(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        self.clinica.registrar_mascota("Otro", "Perro", 3, "Lab", 47111111)

        with self.assertRaises(ValueError):
            self.clinica.agendar_turno("Otro", 47111111, "MAT1", 1, fecha)

    # ❌ mismo consultorio
    def test_turno_mismo_consultorio(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        self.clinica.registrar_veterinario(12345678, "Otro", "01111111111", "MAT2", "General")

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

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, datetime(2032, 12, 12, 10, 0))

        with self.assertRaises(ValueError):
            # mismo veterinario, intervalo solapado (10:00-10:30 vs 10:15-10:45)
            self.clinica.agendar_turno("Luna", 47222222, "MAT1", 2, datetime(2032, 12, 12, 10, 15))

    # ✔ cancelar OK
    def test_cancelar_turno_ok(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        turno_id = self.clinica._turnos[0].get_id()
        self.clinica.cancelar_turno(turno_id)

        self.assertEqual("Cancelado", self.clinica._turnos[0].get_estado())

    # ❌ cancelar inexistente
    def test_cancelar_turno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.cancelar_turno(999)

    # ❌ cancelar dos veces
    def test_cancelar_turno_dos_veces(self):
        fecha = datetime(2032, 12, 12, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)
        turno_id = self.clinica._turnos[0].get_id()

        self.clinica.cancelar_turno(turno_id)

        with self.assertRaises(ValueError):
            self.clinica.cancelar_turno(turno_id)

    # ✔ modificar OK
    def test_modificar_turno_ok(self):
        fecha = datetime(2032, 12, 12, 10, 0)
        nueva = datetime(2032, 12, 13, 10, 0)

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        turno_id = self.clinica._turnos[0].get_id()
        self.clinica.modificar_turno(turno_id, nueva)

        self.assertEqual(nueva, self.clinica._turnos[0].get_fecha_hora())

    # ❌ modificar fecha pasada
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
        self.clinica.registrar_veterinario(12345678, "Otro", "01111111111", "MAT2", "General")

        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, datetime(2032, 12, 12, 10, 0))
        self.clinica.agendar_turno("Mambo", 47111111, "MAT2", 2, datetime(2032, 12, 12, 11, 0))

        turno_a_modificar = self.clinica._turnos[1].get_id()

        with self.assertRaises(ValueError):
            # al mover a 10:15 se solapa con el turno existente de la misma mascota
            self.clinica.modificar_turno(turno_a_modificar, datetime(2032, 12, 12, 10, 15))

    def test_turnos_pegados_no_se_superponen(self):
        self.clinica.registrar_dueno(47222222, "Juan", "01122222222", "Otra")
        self.clinica.registrar_mascota("Luna", "Gato", 3, "Siames", 47222222)
        self.clinica.registrar_veterinario(12345678, "Otro", "01111111111", "MAT2", "General")

        # Primer turno: 10:30-11:00
        self.clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, datetime(2032, 12, 12, 10, 30))

        # Segundo turno: 11:00-11:30 (empieza justo cuando termina el primero)
        # Cambian veterinario, consultorio y mascota para que no haya otra restricción.
        self.clinica.agendar_turno("Luna", 47222222, "MAT2", 1, datetime(2032, 12, 12, 11, 0))

        self.assertEqual(2, len(self.clinica._turnos))

    # ❌ modificar inexistente
    def test_modificar_turno_inexistente(self):
        with self.assertRaises(ValueError):
            self.clinica.modificar_turno(999, datetime(2032, 12, 13, 10, 0))