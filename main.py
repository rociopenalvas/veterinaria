from clinica import ClinicaVeterinaria
from menu import Menu

def main():
    # Crear la clínica que controla los turnos
    clinica = ClinicaVeterinaria("Veterinariaaa")

    # Crear el menú
    menu = Menu(clinica)

    menu.ejecutar()

if __name__ == "__main__":
    main()