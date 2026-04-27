from datetime import datetime
from clinica import ClinicaVeterinaria

class Menu:
    def __init__(self, clinica):
        self._clinica = clinica

    def ejecutar(self):
        while True:
            print("\n===== SISTEMA VETERINARIA =====")
            print("1. Dueños")
            print("2. Mascotas")
            print("3. Veterinarios")
            print("4. Consultorios")
            print("5. Turnos")
            print("0. Salir")

            opcion = input("Seleccione opción: ")

            try:
                if opcion == "1":
                    self._menu_duenos()

                elif opcion == "2":
                    self._menu_mascotas()

                elif opcion == "3":
                    self._menu_veterinarios()

                elif opcion == "4":
                    self._menu_consultorios()

                elif opcion == "5":
                    self._menu_turnos()

                elif opcion == "0":
                    break

                else:
                    print("Opción inválida.")

            except ValueError as e:
                print("Error:", e)

    def _menu_duenos(self):
        while True:
            print("\n--- DUEÑOS ---")
            print("1. Registrar")
            print("2. Listar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    dni = self._pedir_entero("DNI: ")
                    nombre = input("Nombre: ")
                    telefono = input("Teléfono (XXX XXXX-XXXX): ").strip()
                    direccion = input("Dirección: ")

                    self._clinica.registrar_dueno(
                        dni, nombre, telefono, direccion
                    )

                    print("Dueño registrado con éxito.")

                elif opcion == "2":
                    self._clinica.listar_duenos()

                elif opcion == "3":
                    dni = self._pedir_entero("DNI: ")
                    telefono = input("Nuevo teléfono (XXX XXXX-XXXX): ").strip()
                    direccion = input("Nueva dirección: ")

                    self._clinica.modificar_dueno(
                        dni, telefono, direccion
                    )

                    print("Dueño modificado.")

                elif opcion == "4":
                    dni = self._pedir_entero("DNI: ")

                    self._clinica.eliminar_dueno(dni)

                    print("Dueño eliminado.")

                elif opcion == "0":
                    break

                else:
                    print("Opción inválida.")

            except ValueError as e:
                print("Error:", e)

    def _menu_veterinarios(self):
        while True:
            print("\n--- VETERINARIOS ---")
            print("1. Registrar")
            print("2. Listar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    dni = self._pedir_entero("DNI: ")
                    nombre = input("Nombre: ")
                    telefono = input("Teléfono (XXX XXXX-XXXX): ").strip()
                    matricula = input("Matrícula: ")
                    especialidad = input("Especialidad: ")

                    self._clinica.registrar_veterinario(
                        dni, nombre, telefono, matricula, especialidad
                    )

                    print("Veterinario registrado con éxito.")

                elif opcion == "2":
                    self._clinica.listar_veterinarios()

                elif opcion == "3":
                    matricula = input("Matrícula: ")
                    telefono = input("Nuevo teléfono (XXX XXXX-XXXX): ").strip()
                    especialidad = input("Nueva especialidad: ")

                    self._clinica.modificar_veterinario(
                        matricula, telefono, especialidad
                    )

                    print("Veterinario modificado.")

                elif opcion == "4":
                    matricula = input("Matrícula: ")

                    self._clinica.eliminar_veterinario(matricula)

                    print("Veterinario eliminado.")

                elif opcion == "0":
                    break

                else:
                    print("Opción inválida.")

            except ValueError as e:
                print("Error:", e)

    def _menu_consultorios(self):
        while True:
            print("\n--- CONSULTORIOS ---")
            print("1. Registrar")
            print("2. Listar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    numero = self._pedir_entero("Número: ")
                    descripcion = input("Descripción: ")

                    self._clinica.registrar_consultorio(
                        numero, descripcion
                    )

                    print("Consultorio registrado con éxito.")

                elif opcion == "2":
                    self._clinica.listar_consultorios()

                elif opcion == "3":
                    numero = self._pedir_entero("Número: ")
                    descripcion = input("Nueva descripción: ")

                    self._clinica.modificar_consultorio(
                        numero, descripcion
                    )

                    print("Consultorio modificado.")

                elif opcion == "4":
                    numero = self._pedir_entero("Número: ")

                    self._clinica.eliminar_consultorio(numero)

                    print("Consultorio eliminado.")

                elif opcion == "0":
                    break

                else:
                    print("Opción inválida.")

            except ValueError as e:
                print("Error:", e)

    def _menu_mascotas(self):
        while True:
            print("\n--- MASCOTAS ---")
            print("1. Registrar")
            print("2. Listar")
            print("3. Modificar")
            print("4. Eliminar")
            print("0. Volver")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    nombre = input("Nombre: ")
                    especie = input("Especie: ")
                    edad = self._pedir_entero("Edad: ")
                    raza = input("Raza: ")
                    dni_dueno = self._pedir_entero("DNI del dueño: ")

                    self._clinica.registrar_mascota(
                        nombre, especie, edad, raza, dni_dueno
                    )

                    print("Mascota registrada con éxito.")

                elif opcion == "2":
                    self._clinica.listar_mascotas()

                elif opcion == "3":
                    nombre = input("Nombre de la mascota: ")
                    dni_dueno = self._pedir_entero("DNI del dueño: ")
                    nueva_edad = self._pedir_entero("Nueva edad: ")

                    self._clinica.modificar_mascota(
                        nombre, dni_dueno, nueva_edad
                    )

                    print("Mascota modificada.")

                elif opcion == "4":
                    nombre = input("Nombre de la mascota: ")
                    dni_dueno = self._pedir_entero("DNI del dueño: ")

                    self._clinica.eliminar_mascota(
                        nombre, dni_dueno
                    )

                    print("Mascota eliminada.")

                elif opcion == "0":
                    break

                else:
                    print("Opción inválida.")

            except ValueError as e:
                print("Error:", e) 
    
    def _menu_turnos(self):
        while True:
            print("\n--- TURNOS ---")
            print("1. Agendar")
            print("2. Listar")
            print("3. Modificar fecha")
            print("4. Cancelar")
            print("5. Consultas")
            print("0. Volver")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    self._agendar_turno()

                elif opcion == "2":
                    self._clinica.listar_turnos()

                elif opcion == "3":
                    self._modificar_turno()

                elif opcion == "4":
                    self._cancelar_turno()

                elif opcion == "5":
                    self._consultas_turnos()

                elif opcion == "0":
                    break

                else:
                    print("Opción inválida.")

            except ValueError as e:
                print("Error:", e)

    def _pedir_fecha_hora(self):
        texto = input("Fecha y hora (YYYY-MM-DD HH:MM): ")

        try:
            fecha = datetime.strptime(texto, "%Y-%m-%d %H:%M")
            return fecha

        except ValueError:
            raise ValueError("Formato de fecha inválido.") 
    
    def _agendar_turno(self):
        nombre = input("Nombre mascota: ")
        dni = self._pedir_entero("DNI dueño: ")
        matricula = input("Matrícula veterinario: ")
        numero = self._pedir_entero("Número consultorio: ")

        fecha = self._pedir_fecha_hora()

        self._clinica.agendar_turno(
            nombre,
            dni,
            matricula,
            numero,
            fecha
        )

    def _modificar_turno(self):
            id_turno = int(input("ID del turno: "))
            nueva_fecha = self._pedir_fecha_hora()

            self._clinica.modificar_turno(
                id_turno,
                nueva_fecha
            )

            print("Turno modificado.")
            print("Turno agendado con éxito.")

    def _cancelar_turno(self):
        id_turno = int(input("ID del turno: "))

        self._clinica.cancelar_turno(id_turno)

        print("Turno cancelado.")

    def _consultas_turnos(self):
        while True:
            print("\n--- CONSULTAS DE TURNOS ---")
            print("1. Por fecha")
            print("2. Por veterinario")
            print("3. Por mascota")
            print("4. Por dueño")
            print("0. Volver")

            opcion = input("Opción: ")

            try:
                if opcion == "1":
                    self._consulta_por_fecha()

                elif opcion == "2":
                    self._consulta_por_veterinario()

                elif opcion == "3":
                    self._consulta_por_mascota()

                elif opcion == "4":
                    self._consulta_por_dueno()

                elif opcion == "0":
                    break

                else:
                    print("Opción inválida.")

            except ValueError as e:
                print("Error:", e) 
            
    def _consulta_por_fecha(self):
        texto = input("Ingrese fecha (YYYY-MM-DD): ")

        try:
            fecha = datetime.strptime(texto, "%Y-%m-%d").date()

        except ValueError:
            raise ValueError("Fecha inválida.")

        resultados = self._clinica.turnos_por_fecha(fecha)

        self._mostrar_resultados(resultados)

    def _consulta_por_veterinario(self):
        matricula = input("Matrícula: ")

        resultados = self._clinica.turnos_por_veterinario(matricula)

        self._mostrar_resultados(resultados)

    def _consulta_por_mascota(self):
        nombre = input("Nombre mascota: ")
        dni = self._pedir_entero("DNI dueño: ")

        resultados = self._clinica.turnos_por_mascota(nombre, dni)

        self._mostrar_resultados(resultados)

    def _consulta_por_dueno(self):
        dni = self._pedir_entero("DNI dueño: ")

        resultados = self._clinica.turnos_por_dueno(dni)

        self._mostrar_resultados(resultados)

    def _mostrar_resultados(self, resultados):
        if not resultados:
            print("No se encontraron turnos.")
            return

        for turno in resultados:
            print("------------------")
            turno.mostrar_info()

    def _pedir_entero(self, mensaje):
        try:
            return int(input(mensaje))
        except ValueError:
            raise ValueError("Debe ingresar un número válido.")