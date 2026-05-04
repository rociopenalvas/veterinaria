import json

from clinica import ClinicaVeterinaria
from dao.clinica_dao import ClinicaDAO
from menu import Menu


def main():
    """Inicializa la app, carga datos, ejecuta menú y persiste cambios."""

    clinica = ClinicaVeterinaria("Veterinaria Reneé 81")
    dao = ClinicaDAO()

    try:
        dao.cargar(clinica, "data/")
    except FileNotFoundError:
        pass
    except json.JSONDecodeError as e:
        print("Error: un archivo en data/ no es JSON válido.", e)
    except (ValueError, KeyError) as e:
        print("Error al cargar datos (dato repetido, incompleto o turno inválido):", e)

    menu = Menu(clinica)
    menu.ejecutar()
    dao.guardar(clinica, "data/")


if __name__ == "__main__":
    main()
