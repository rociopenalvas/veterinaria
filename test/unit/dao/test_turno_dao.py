import unittest
from datetime import datetime
from clinica import ClinicaVeterinaria
from dao.dueno_dao import DuenoDAO
from dao.mascota_dao import MascotaDAO
from dao.veterinario_dao import VeterinarioDAO
from dao.consultorio_dao import ConsultorioDAO
from dao.turno_dao import TurnoDAO


class TestTurnoDAO(unittest.TestCase):

    def test_guardar_y_cargar_turnos(self):
        clinica = ClinicaVeterinaria("Test")

        # base completa
        clinica.registrar_dueno(47111111, "Soledad", "01136111111", "Calle")
        clinica.registrar_mascota("Mambo", "Perro", 5, "Lab", 47111111)
        clinica.registrar_veterinario(87654321, "Dr", "10987654321", "MAT1", "General")
        clinica.registrar_consultorio(1, "C1")

        fecha = datetime(2032, 12, 12, 10, 0)

        clinica.agendar_turno("Mambo", 47111111, "MAT1", 1, fecha)

        # DAO
        dao_dueno = DuenoDAO()
        dao_mascota = MascotaDAO()
        dao_vet = VeterinarioDAO()
        dao_cons = ConsultorioDAO()
        dao_turno = TurnoDAO()

        # guardar
        dao_dueno.guardar(clinica._duenos, "test_data/duenos.json")
        dao_mascota.guardar(clinica._mascotas, "test_data/mascotas.json")
        dao_vet.guardar(clinica._veterinarios, "test_data/veterinarios.json")
        dao_cons.guardar(clinica._consultorios, "test_data/consultorios.json")
        dao_turno.guardar(clinica._turnos, "test_data/turnos.json")

        # cargar
        nueva = ClinicaVeterinaria("Nueva")

        dao_dueno.cargar("test_data/duenos.json", nueva)
        dao_mascota.cargar("test_data/mascotas.json", nueva)
        dao_vet.cargar("test_data/veterinarios.json", nueva)
        dao_cons.cargar("test_data/consultorios.json", nueva)
        dao_turno.cargar("test_data/turnos.json", nueva)

        self.assertEqual(1, len(nueva._turnos))

        t = nueva._turnos[0]

        self.assertEqual("Mambo", t.get_mascota().get_nombre())
        self.assertEqual("MAT1", t.get_veterinario().get_matricula())