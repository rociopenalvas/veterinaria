from dao.dueno_dao import DuenoDAO
from dao.mascota_dao import MascotaDAO
from dao.veterinario_dao import VeterinarioDAO
from dao.consultorio_dao import ConsultorioDAO
from dao.turno_dao import TurnoDAO


class ClinicaDAO:

    def __init__(self):
        self.dueno_dao = DuenoDAO()
        self.mascota_dao = MascotaDAO()
        self.vet_dao = VeterinarioDAO()
        self.cons_dao = ConsultorioDAO()
        self.turno_dao = TurnoDAO()

    def guardar(self, clinica, base_path):
        self.dueno_dao.guardar(clinica._duenos, base_path + "duenos.json")
        self.mascota_dao.guardar(clinica._mascotas, base_path + "mascotas.json")
        self.vet_dao.guardar(clinica._veterinarios, base_path + "veterinarios.json")
        self.cons_dao.guardar(clinica._consultorios, base_path + "consultorios.json")
        self.turno_dao.guardar(clinica._turnos, base_path + "turnos.json")

    def cargar(self, clinica, base_path):
        self.dueno_dao.cargar(base_path + "duenos.json", clinica)
        self.mascota_dao.cargar(base_path + "mascotas.json", clinica)
        self.vet_dao.cargar(base_path + "veterinarios.json", clinica)
        self.cons_dao.cargar(base_path + "consultorios.json", clinica)
        self.turno_dao.cargar(base_path + "turnos.json", clinica)