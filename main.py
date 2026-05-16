import json

from clinica import ClinicaVeterinaria
from dao.clinica_dao import ClinicaDAO
from menu import Menu


def main():
    """Inicializa la app, carga datos, ejecuta menú y persiste cambios."""

    clinica = ClinicaVeterinaria("Veterinaria Lorde 81")
    dao = ClinicaDAO()

    # El sistema valida que no haya datos inconsistentes al cargar.
    try:
        dao.cargar(clinica, "data/")
    # Si algún archivo falta la primera vez, comenzaremos con datos vacíos
    except FileNotFoundError:
        pass
    # Si hay un archivo JSON mal formado, comunicamos al usuario
    except json.JSONDecodeError as e:
        print("Error: un archivo en data/ no es JSON válido.", e)
    # Hay datos inválidos según la lógica (duplicado, incompleto, superpuesto)
    except (ValueError, KeyError) as e:
        print("Error al cargar (repetido, incompleto, turno inválido):", e)

    menu = Menu(clinica)
    menu.ejecutar()
    dao.guardar(clinica, "data/")


if __name__ == "__main__":
    main()
