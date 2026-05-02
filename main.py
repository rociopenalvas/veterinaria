import json

from clinica import ClinicaVeterinaria
from dao.clinica_dao import ClinicaDAO
from menu import Menu

def main():
    # Crear la clínica
    clinica = ClinicaVeterinaria("VVeterinariaaa")

    # Crear DAO
    dao = ClinicaDAO()

    # Cargar datos si existen archivos en data/
    try:
        dao.cargar(clinica, "data/")
    except FileNotFoundError:
        pass  # primera ejecución o todavía no guardaste nada
    except json.JSONDecodeError as e:
        print("Error: un archivo en data/ no es JSON válido.", e)
    except (ValueError, KeyError) as e:
        print("Error al cargar datos (dato repetido, incompleto o turno inválido):", e)

    # Crear menú
    menu = Menu(clinica)

    # Ejecutar programa
    menu.ejecutar()

    # 🔽 GUARDAR DATOS al salir
    dao.guardar(clinica, "data/")

if __name__ == "__main__":
    main()