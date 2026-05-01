from modelo.turno import Turno
from modelo.mascota import Mascota
from modelo.veterinario import Veterinario
from modelo.consultorio import Consultorio
from modelo.dueno import Dueno
from datetime import date


class ClinicaVeterinaria:
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._mascotas = []
        self._veterinarios = []
        self._consultorios = []
        self._turnos = []
        self._duenos = []

    def registrar_veterinario(self, dni: int, nombre: str, telefono: str, matricula: str, especialidad: str):
        if dni < 10000000 or dni > 99999999:
            raise ValueError("DNI inválido.")

        if nombre.strip() == "" or nombre.isdigit():
            raise ValueError("Nombre inválido.")

        if not telefono.isdigit() or len(telefono) != 11:
            raise ValueError("Teléfono inválido.")

        if matricula.strip() == "":
            raise ValueError("Matrícula inválida.")

        if especialidad.strip() == "":
            raise ValueError("Especialidad inválida.")

        if self._buscar_veterinario_por_matricula(matricula) is not None:
            raise ValueError("La matricula ya está registrada.")
        
        veterinario = Veterinario(dni, nombre, telefono, matricula, especialidad)
        self._veterinarios.append(veterinario)

    def registrar_consultorio(self, numero: int, descripcion: str):
        if numero <= 0:
            raise ValueError("Número de consultorio inválido.")

        if descripcion.strip() == "":
            raise ValueError("Descripción inválida.")

        if self._buscar_consultorio_por_numero(numero) is not None:
            raise ValueError("Ya existe un consultorio con ese número.")
        
        consultorio = Consultorio(numero, descripcion)
        self._consultorios.append(consultorio)

    def registrar_dueno(self, dni: int, nombre: str, telefono: str, direccion: str):
        if dni < 10000000 or dni > 99999999:
            raise ValueError("DNI inválido.")

        if nombre.strip() == "" or nombre.isdigit():
            raise ValueError("Nombre inválido.")

        if not telefono.isdigit() or len(telefono) != 11:
            raise ValueError("Teléfono inválido.")

        if direccion.strip() == "":
            raise ValueError("Dirección inválida.")

        if self._buscar_dueno_por_dni(dni) is not None:
            raise ValueError("El DNI ya está registrado.")
    
        dueno = Dueno(dni, nombre, telefono, direccion)
        self._duenos.append(dueno)

    def _hay_problema(self, turno: Turno, nueva_fecha=None) -> bool:
        """
        Verifica si un turno se superpone con otro activo.
        Si nueva_fecha no es None, se usa esa fecha en vez de la original.
        """
        fecha = nueva_fecha if nueva_fecha else turno.get_fecha_hora()

        for t in self._turnos:
            # Mismo veterinario y misma fecha/hora
            if (
                t.get_veterinario() == turno.get_veterinario()
                and t.get_fecha_hora() == fecha
                and t.get_estado() == "Activo"
            ):
                raise ValueError("El veterinario ya tiene un turno en ese horario.")

            # Mismo consultorio y misma fecha/hora
            if (
                t.get_consultorio() == turno.get_consultorio()
                and t.get_fecha_hora() == fecha
                and t.get_estado() == "Activo"
            ):
                raise ValueError("El consultorio ya está ocupado en ese horario.")
            
            # Misma mascota y misma fecha/hora
            if (
                t.get_mascota() == turno.get_mascota()
                and t.get_fecha_hora() == fecha
                and t.get_estado() == "Activo"
            ):
                raise ValueError("La mascota ya tiene turno en ese horario.")

    def agendar_turno(self, nombre_mascota: str, dni_dueno: int, matricula: str, numero_consultorio: int, fecha_hora):
        """
        Agenda un turno si no hay superposición con turnos activos.
        """ 
        # Validar datos básicos
        if nombre_mascota.strip() == "":
            raise ValueError("Nombre de mascota inválido.")

        if dni_dueno < 10000000 or dni_dueno > 99999999:
            raise ValueError("DNI inválido.")

        if matricula.strip() == "":
            raise ValueError("Matrícula inválida.")

        if numero_consultorio <= 0:
            raise ValueError("Número de consultorio inválido.")

        # Buscar dueño
        dueno = self._buscar_dueno_por_dni(dni_dueno)
        if dueno is None:
            raise ValueError("El dueño no existe.")

        # Buscar mascota
        mascota = self._buscar_mascota(nombre_mascota, dni_dueno)
        if mascota is None:
            raise ValueError("La mascota no existe.")

        # Buscar veterinario
        veterinario = self._buscar_veterinario_por_matricula(matricula)
        if veterinario is None:
            raise ValueError("El veterinario no existe.")

        # Buscar consultorio
        consultorio = self._buscar_consultorio_por_numero(numero_consultorio)
        if consultorio is None:
            raise ValueError("El consultorio no existe.")

        turno = Turno(mascota, veterinario, fecha_hora, consultorio)
        
        # Validar superposición
        self._hay_problema(turno)
        # Si pasa las validaciones, se agenda
        self._turnos.append(turno)

    def listar_turnos(self):
        """
        Muestra todos los turnos registrados.
        """
        print(f"\nTurnos en {self._nombre}:")
        for turno in self._turnos:
            turno.mostrar_info()
            print("-------------------")

    def _buscar_turno_por_id(self, id_turno: int) -> Turno:
        """
        Busca un turno en la lista por su Id, verificando su existencia.
        """
        for turno in self._turnos:
            if turno.get_id() == id_turno:
                return turno 
            
        raise ValueError("El turno no existe.")
    
    def registrar_mascota(self, nombre, especie, edad, raza, dni_dueno):
        if nombre.strip() == "" or nombre.isdigit():
            raise ValueError("Nombre inválido.")

        if especie.strip() == "" or nombre.isdigit():
            raise ValueError("Especie inválida.")

        if raza.strip() == "":
            raise ValueError("Raza inválida.")

        if edad < 0:
            raise ValueError("Edad inválida.")

        if dni_dueno < 10000000 or dni_dueno > 99999999:
            raise ValueError("DNI inválido.")

        dueno = self._buscar_dueno_por_dni(dni_dueno)

        # verificar que existge el dueno
        if dueno is None:
            raise ValueError("El dueño no existe. Debe registrarse primero.")

        # verificar duplicado
        if self._buscar_mascota(nombre, dni_dueno) is not None:
            raise ValueError("Ya existe una mascota con ese nombre para ese dueño.")

        mascota = Mascota(especie, edad, nombre, raza, dueno)
        self._mascotas.append(mascota)

    def eliminar_mascota(self, nombre: str, dni_dueno: int):
        dueno = self._buscar_dueno_por_dni(dni_dueno)

        # verificar dueno
        if dueno is None:
            raise ValueError("El dueño no existe.")

        mascota = self._buscar_mascota(nombre, dni_dueno)

        if mascota is None:
            raise ValueError("La mascota no existe.")

        # verificar turnos asociados
        for turno in self._turnos:
            if turno.get_mascota() == mascota:
                raise ValueError("No se puede eliminar la mascota porque tiene turnos asociados.")

        self._mascotas.remove(mascota)

    def _buscar_mascota(self, nombre: str, dni_dueno: int) -> Mascota:
        for mascota in self._mascotas:
            if mascota.get_nombre() == nombre and mascota.get_dueno().get_dni() == dni_dueno:
                return mascota
        return None 
    
    def listar_mascotas(self):
        if not self._mascotas:
            print("No hay mascotas registradas.")
            return

        for mascota in self._mascotas:
            print("------------------")
            mascota.mostrar_info()
    
    def modificar_mascota(self, nombre: str, dni_dueno: int, nueva_edad: int):
        dueno = self._buscar_dueno_por_dni(dni_dueno)

        # verificar dueno
        if dueno is None:
            raise ValueError("El dueño no existe.")
        

        mascota = self._buscar_mascota(nombre, dni_dueno)

        if mascota is None:
            raise ValueError("La mascota no existe.")
        
        if nueva_edad < 0:
            raise ValueError("Edad inválida.")

        mascota.set_edad(nueva_edad)

    def cancelar_turno(self, id_turno: int):
        """
        Cancela un turno existente.
        """
        turno = self._buscar_turno_por_id(id_turno)

        if turno is None:
            raise ValueError("El turno no existe.")

        if turno.get_estado() == "Cancelado":
            raise ValueError("El turno ya estaba cancelado.")

        turno.cancelar()

    def modificar_turno(self, id_turno: int, nueva_fecha):

        turno = self._buscar_turno_por_id(id_turno)

        if turno is None:
            raise ValueError("El turno no existe.")

        self._hay_problema(turno, nueva_fecha)

        turno.modificar_fecha(nueva_fecha)

    def turnos_por_veterinario(self, matricula_veterinario: str):
        resultados = []
        for t in self._turnos:
            if t.get_veterinario() == self._buscar_veterinario_por_matricula(matricula_veterinario) and t.get_estado() == "Activo":
                resultados.append(t)
        return resultados
            
    def turnos_por_mascota(self, nombre_mascota: str, dni_dueno: int):
        resultados = []
        for t in self._turnos:
            if t.get_mascota() == self._buscar_mascota(nombre_mascota, dni_dueno) and t.get_estado() == "Activo":
                resultados.append(t)
        return resultados
    
    def turnos_por_dueno(self, dni_dueno: int):
        resultados = []
        for t in self._turnos:
            if t.get_mascota().get_dueno() == self._buscar_dueno_por_dni(dni_dueno) and t.get_estado() == "Activo":
                resultados.append(t)
        return resultados
    
    def turnos_por_fecha(self, fecha: date):
        resultados = []
        for t in self._turnos:
            if t.get_fecha_hora().date() == fecha and t.get_estado() == "Activo":
                resultados.append(t)
        return resultados
    
    def _buscar_dueno_por_dni(self, dni: int) -> Dueno:
        """
        Busca un dueno en la lista por su dni.
        """
        for dueno in self._duenos:
            if dueno.get_dni() == dni:
                return dueno
        return None
    
    def eliminar_dueno(self, dni: int):
        dueno = self._buscar_dueno_por_dni(dni)

        if dueno is None:
            raise ValueError("El dueño no existe.")

        # Verificar si tiene mascotas asociadas
        for mascota in self._mascotas:
            if mascota.get_dueno() == dueno:
                raise ValueError("No se puede eliminar dueño porque tiene mascotas asociadas.")

        self._duenos.remove(dueno)

    def modificar_dueno(self, dni: int, nuevo_telefono: str, nueva_direccion: str):
        dueno = self._buscar_dueno_por_dni(dni)

        if dueno is None:
            raise ValueError("El dueño no existe.")
        
        if not nuevo_telefono.isdigit() or len(nuevo_telefono) != 11:
            raise ValueError("Teléfono inválido.")

        if nueva_direccion.strip() == "":
            raise ValueError("Dirección inválida.")

        dueno.set_telefono(nuevo_telefono)
        dueno.set_direccion(nueva_direccion)

    def listar_duenos(self):
        if not self._duenos:
            print("No hay dueños registrados.")
            return

        for dueno in self._duenos:
            print("------------------")
            dueno.mostrar_info() 
    
    def _buscar_veterinario_por_matricula(self, matricula: str) -> Veterinario:
        """
        Busca un veterinario en la lista por su matricula.
        """
        for veterinario in self._veterinarios:
            if veterinario.get_matricula() == matricula:
                return veterinario
        return None 

    def eliminar_veterinario(self, matricula: str):
        veterinario = self._buscar_veterinario_por_matricula(matricula)

        if veterinario is None:
            raise ValueError("El veterinario no existe.")

        # Verificar si tiene turnos asociados
        for turno in self._turnos:
            if turno.get_veterinario() == veterinario:
                raise ValueError("El veterinario porque tiene turnos asociados.")
            
        self._veterinarios.remove(veterinario)

    def modificar_veterinario(self, matricula: str, nuevo_telefono: str, nueva_especialidad: str):
        veterinario = self._buscar_veterinario_por_matricula(matricula)

        if veterinario is None:
            raise ValueError("El veterinario no existe.")

        if not nuevo_telefono.isdigit() or len(nuevo_telefono) != 11:
            raise ValueError("Teléfono inválido.")

        if nueva_especialidad.strip() == "":
            raise ValueError("Especialidad inválida.")

        veterinario.set_telefono(nuevo_telefono)
        veterinario.set_especialidad(nueva_especialidad)

    def listar_veterinarios(self):
        if not self._veterinarios:
            print("No hay veterinarios registrados.")
            return

        for veterinario in self._veterinarios:
            print("------------------")
            veterinario.mostrar_info()

    def modificar_consultorio(self, numero: int, nueva_descripcion: str):
        consultorio = self._buscar_consultorio_por_numero(numero)

        if consultorio is None:
            raise ValueError("El consultorio no existe.")
        
        if nueva_descripcion.strip() == "":
            raise ValueError("Descripción inválida.")

        consultorio.set_descripcion(nueva_descripcion)

    def _buscar_consultorio_por_numero(self, numero: int) -> Consultorio:
        """
        Busca un consultorio en la lista por su número.
        """
        for consultorio in self._consultorios:
            if consultorio.get_numero() == numero:
                return consultorio
        return None

    def eliminar_consultorio(self, numero: int):
        consultorio = self._buscar_consultorio_por_numero(numero)

        if consultorio is None:
            raise ValueError("El consultorio no existe.")

        # verificar turnos asignados al consultorio
        for turno in self._turnos:
            if turno.get_consultorio() == consultorio:
                raise ValueError("No se puede eliminar el consultorio porque tiene turnos asociados.")

        self._consultorios.remove(consultorio)

    def listar_consultorios(self):
        if not self._consultorios:
            print("No hay consultorios registrados.")
            return

        for consultorio in self._consultorios:
            print("------------------")
            consultorio.mostrar_info()