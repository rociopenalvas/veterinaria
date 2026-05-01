from clinica import ClinicaVeterinaria
from dao.clinica_dao import ClinicaDAO
from menu import Menu

def main():
    # Crear la clínica
    clinica = ClinicaVeterinaria("VVeterinariaaa")

    # Crear DAO
    dao = ClinicaDAO()

    # 🔽 CARGAR DATOS (si existen)
    try:
        dao.cargar(clinica, "data/")
    except:
        pass  # si no hay archivos todavía, no pasa nada

    # Crear menú
    menu = Menu(clinica)

    # Ejecutar programa
    menu.ejecutar()

    # 🔽 GUARDAR DATOS al salir
    dao.guardar(clinica, "data/")

if __name__ == "__main__":
    main()