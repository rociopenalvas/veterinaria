from datetime import date, datetime, timedelta

from modelo.consultorio import Consultorio
from modelo.dueno import Dueno
from modelo.mascota import Mascota
from modelo.turno import Turno
from modelo.veterinario import Veterinario


class ClinicaVeterinaria:
    """Orquesta la lógica de negocio de la clínica veterinaria."""

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._mascotas = []
        self._veterinarios = []
        self._consultorios = []
        self._turnos = []
        self._duenos = []

    def registrar_veterinario(
        self, dni: int, nombre: str, telefono: str, matricula: str, especialidad: str
    ) -> None:
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

    def registrar_consultorio(self, numero: int, descripcion: str) -> None:
        if numero <= 0:
            raise ValueError("Número de consultorio inválido.")

        if descripcion.strip() == "":
            raise ValueError("Descripción inválida.")

        if self._buscar_consultorio_por_numero(numero) is not None:
            raise ValueError("Ya existe un consultorio con ese número.")

        consultorio = Consultorio(numero, descripcion)
        self._consultorios.append(consultorio)

    def registrar_dueno(
        self, dni: int, nombre: str, telefono: str, direccion: str
    ) -> None:
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

    def _verificar_superposicion_turno(self, turno: Turno, nueva_fecha=None):
        """
        Verifica si un turno se superpone con otro activo.
        Si nueva_fecha no es None, se usa esa fecha en vez de la original.
        """
        # Solapamiento de intervalos [inicio, fin); nueva_fecha = al modificar un turno.
        inicio_nuevo = nueva_fecha if nueva_fecha else turno.get_fecha_hora()
        fin_nuevo = inicio_nuevo + timedelta(minutes=Turno.DURACION_MINUTOS)

        for t in self._turnos:
            if t.get_estado() != "Activo":
                continue

            if t.get_id() == turno.get_id():
                continue

            inicio_existente = t.get_fecha_hora()
            fin_existente = t.get_fecha_fin()

            # Dos turnos se superponen si el inicio de uno es antes del fin del otro
            # y al revés (intervalos [inicio, fin)).
            se_superpone = inicio_nuevo < fin_existente and inicio_existente < fin_nuevo

            if not se_superpone:
                continue

            if (
                t.get_veterinario() == turno.get_veterinario()
            ):
                raise ValueError("El veterinario ya tiene un turno en ese horario.")

            if (
                t.get_consultorio() == turno.get_consultorio()
            ):
                raise ValueError("El consultorio ya está ocupado en ese horario.")

            if (
                t.get_mascota() == turno.get_mascota()
            ):
                raise ValueError("La mascota ya tiene turno en ese horario.")

    def _turno_activo_futuro(self, turno: Turno) -> bool:
        activo = turno.get_estado() == "Activo"
        futuro = turno.get_fecha_hora() >= datetime.now()
        return activo and futuro

    def agendar_turno(
        self,
        nombre_mascota: str,
        dni_dueno: int,
        matricula: str,
        numero_consultorio: int,
        fecha_hora,
    ) -> None:
        if nombre_mascota.strip() == "":
            raise ValueError("Nombre de mascota inválido.")

        if dni_dueno < 10000000 or dni_dueno > 99999999:
            raise ValueError("DNI inválido.")

        if matricula.strip() == "":
            raise ValueError("Matrícula inválida.")

        if numero_consultorio <= 0:
            raise ValueError("Número de consultorio inválido.")

        dueno = self._buscar_dueno_por_dni(dni_dueno)
        if dueno is None:
            raise ValueError("El dueño no existe.")

        mascota = self._buscar_mascota(nombre_mascota, dni_dueno)
        if mascota is None:
            raise ValueError("La mascota no existe.")

        veterinario = self._buscar_veterinario_por_matricula(matricula)
        if veterinario is None:
            raise ValueError("El veterinario no existe.")

        consultorio = self._buscar_consultorio_por_numero(numero_consultorio)
        if consultorio is None:
            raise ValueError("El consultorio no existe.")

        turno = Turno(mascota, veterinario, fecha_hora, consultorio)

        self._verificar_superposicion_turno(turno)
        self._turnos.append(turno)

    def restaurar_turno(
        self,
        nombre_mascota: str,
        dni_dueno: int,
        matricula: str,
        numero_consultorio: int,
        fecha_hora,
        id_turno: int,
        estado: str,
    ):
        """
        Reconstruye un turno desde JSON (id y estado obligatorios en el archivo).
        No exige fecha futura: sirve para cargar datos persistidos.
        """
        if nombre_mascota.strip() == "":
            raise ValueError("Nombre de mascota inválido.")

        if dni_dueno < 10000000 or dni_dueno > 99999999:
            raise ValueError("DNI inválido.")

        if matricula.strip() == "":
            raise ValueError("Matrícula inválida.")

        if numero_consultorio <= 0:
            raise ValueError("Número de consultorio inválido.")

        dueno = self._buscar_dueno_por_dni(dni_dueno)
        if dueno is None:
            raise ValueError("El dueño no existe.")

        mascota = self._buscar_mascota(nombre_mascota, dni_dueno)
        if mascota is None:
            raise ValueError("La mascota no existe.")

        veterinario = self._buscar_veterinario_por_matricula(matricula)
        if veterinario is None:
            raise ValueError("El veterinario no existe.")

        consultorio = self._buscar_consultorio_por_numero(numero_consultorio)
        if consultorio is None:
            raise ValueError("El consultorio no existe.")

        if estado not in ("Activo", "Cancelado"):
            estado = "Activo"

        turno = Turno(
            mascota,
            veterinario,
            fecha_hora,
            consultorio,
            id_existente=id_turno,
            estado=estado,
            validar_fecha_futura=False,
        )
        self._verificar_superposicion_turno(turno)
        self._turnos.append(turno)

    def listar_turnos_proximos(self):
        ahora = datetime.now()
        proximos = [t for t in self._turnos if t.get_fecha_hora() > ahora]
        proximos.sort(key=lambda t: t.get_fecha_hora())

        print(f"\nPróximos turnos en {self._nombre}:")
        if not proximos:
            print("No hay próximos turnos.")
            return
        for turno in proximos:
            turno.mostrar_info()
            print("-------------------")

    def listar_turnos_pasados(self):
        ahora = datetime.now()
        pasados = [t for t in self._turnos if t.get_fecha_hora() <= ahora]
        pasados.sort(key=lambda t: t.get_fecha_hora(), reverse=True)

        print(f"\nTurnos pasados en {self._nombre}:")
        if not pasados:
            print("No hay turnos pasados.")
            return
        for turno in pasados:
            turno.mostrar_info()
            print("-------------------")

    def _buscar_turno_por_id(self, id_turno: int) -> Turno:
        for turno in self._turnos:
            if turno.get_id() == id_turno:
                return turno

        raise ValueError("El turno no existe.")

    def registrar_mascota(
        self, nombre: str, especie: str, edad: int, raza: str, dni_dueno: int
    ) -> None:
        if nombre.strip() == "" or nombre.isdigit():
            raise ValueError("Nombre inválido.")

        if especie.strip() == "" or especie.isdigit():
            raise ValueError("Especie inválida.")

        if raza.strip() == "":
            raise ValueError("Raza inválida.")

        if edad < 0:
            raise ValueError("Edad inválida.")

        if dni_dueno < 10000000 or dni_dueno > 99999999:
            raise ValueError("DNI inválido.")

        dueno = self._buscar_dueno_por_dni(dni_dueno)

        if dueno is None:
            raise ValueError("El dueño no existe. Debe registrarse primero.")

        if self._buscar_mascota(nombre, dni_dueno) is not None:
            raise ValueError("Ya existe una mascota con ese nombre para ese dueño.")

        mascota = Mascota(especie, edad, nombre, raza, dueno)
        self._mascotas.append(mascota)

    def eliminar_mascota(self, nombre: str, dni_dueno: int) -> None:
        dueno = self._buscar_dueno_por_dni(dni_dueno)
        if dueno is None:
            raise ValueError("El dueño no existe.")

        mascota = self._buscar_mascota(nombre, dni_dueno)

        if mascota is None:
            raise ValueError("La mascota no existe.")

        for turno in self._turnos:
            if turno.get_mascota() == mascota and self._turno_activo_futuro(turno):
                raise ValueError(
                    "No se puede eliminar la mascota porque tiene "
                    "turnos activos futuros asociados."
                )

        self._mascotas.remove(mascota)

    def _buscar_mascota(self, nombre: str, dni_dueno: int) -> Mascota:
        for mascota in self._mascotas:
            dn = mascota.get_dueno().get_dni()
            if mascota.get_nombre() == nombre and dn == dni_dueno:
                return mascota
        return None

    def listar_mascotas(self) -> None:
        if not self._mascotas:
            print("No hay mascotas registradas.")
            return

        for mascota in self._mascotas:
            print("------------------")
            mascota.mostrar_info()

    def modificar_mascota(self, nombre: str, dni_dueno: int, nueva_edad: int) -> None:
        dueno = self._buscar_dueno_por_dni(dni_dueno)
        if dueno is None:
            raise ValueError("El dueño no existe.")

        mascota = self._buscar_mascota(nombre, dni_dueno)

        if mascota is None:
            raise ValueError("La mascota no existe.")

        if nueva_edad < 0:
            raise ValueError("Edad inválida.")

        mascota.set_edad(nueva_edad)

    def cancelar_turno(self, id_turno: int) -> None:
        turno = self._buscar_turno_por_id(id_turno)

        if turno.get_estado() == "Cancelado":
            raise ValueError("El turno ya estaba cancelado.")

        turno.cancelar()

    def modificar_turno(self, id_turno: int, nueva_fecha) -> None:
        """Modifica la fecha de un turno existente."""
        turno = self._buscar_turno_por_id(id_turno)

        self._verificar_superposicion_turno(turno, nueva_fecha)

        turno.modificar_fecha(nueva_fecha)

    def turnos_por_veterinario(self, matricula_veterinario: str):
        resultados = []
        veterinario = self._buscar_veterinario_por_matricula(matricula_veterinario)
        for t in self._turnos:
            if t.get_veterinario() == veterinario and t.get_estado() == "Activo":
                resultados.append(t)
        return resultados

    def turnos_por_mascota(self, nombre_mascota: str, dni_dueno: int):
        resultados = []
        mascota = self._buscar_mascota(nombre_mascota, dni_dueno)
        for t in self._turnos:
            if t.get_mascota() == mascota and t.get_estado() == "Activo":
                resultados.append(t)
        return resultados

    def turnos_por_dueno(self, dni_dueno: int):
        resultados = []
        dueno = self._buscar_dueno_por_dni(dni_dueno)
        for t in self._turnos:
            if t.get_mascota().get_dueno() == dueno and t.get_estado() == "Activo":
                resultados.append(t)
        return resultados

    def turnos_por_fecha(self, fecha: date):
        resultados = []
        for t in self._turnos:
            if t.get_fecha_hora().date() == fecha and t.get_estado() == "Activo":
                resultados.append(t)
        return resultados

    def _buscar_dueno_por_dni(self, dni: int) -> Dueno:
        for dueno in self._duenos:
            if dueno.get_dni() == dni:
                return dueno
        return None

    def eliminar_dueno(self, dni: int) -> None:
        dueno = self._buscar_dueno_por_dni(dni)

        if dueno is None:
            raise ValueError("El dueño no existe.")

        for mascota in self._mascotas:
            if mascota.get_dueno() == dueno:
                raise ValueError(
                    "No se puede eliminar dueño porque tiene mascotas asociadas."
                )

        self._duenos.remove(dueno)

    def modificar_dueno(
        self, dni: int, nuevo_telefono: str, nueva_direccion: str
    ) -> None:
        dueno = self._buscar_dueno_por_dni(dni)

        if dueno is None:
            raise ValueError("El dueño no existe.")

        if not nuevo_telefono.isdigit() or len(nuevo_telefono) != 11:
            raise ValueError("Teléfono inválido.")

        if nueva_direccion.strip() == "":
            raise ValueError("Dirección inválida.")

        dueno.set_telefono(nuevo_telefono)
        dueno.set_direccion(nueva_direccion)

    def listar_duenos(self) -> None:
        if not self._duenos:
            print("No hay dueños registrados.")
            return

        for dueno in self._duenos:
            print("------------------")
            dueno.mostrar_info()

    def _buscar_veterinario_por_matricula(self, matricula: str) -> Veterinario:
        for veterinario in self._veterinarios:
            if veterinario.get_matricula() == matricula:
                return veterinario
        return None

    def eliminar_veterinario(self, matricula: str) -> None:
        veterinario = self._buscar_veterinario_por_matricula(matricula)

        if veterinario is None:
            raise ValueError("El veterinario no existe.")

        for turno in self._turnos:
            mismo_vet = turno.get_veterinario() == veterinario
            if mismo_vet and self._turno_activo_futuro(turno):
                raise ValueError(
                    "No se puede eliminar porque tiene turnos "
                    "activos futuros asociados."
                )

        self._veterinarios.remove(veterinario)

    def modificar_veterinario(
        self, matricula: str, nuevo_telefono: str, nueva_especialidad: str
    ) -> None:
        veterinario = self._buscar_veterinario_por_matricula(matricula)

        if veterinario is None:
            raise ValueError("El veterinario no existe.")

        if not nuevo_telefono.isdigit() or len(nuevo_telefono) != 11:
            raise ValueError("Teléfono inválido.")

        if nueva_especialidad.strip() == "":
            raise ValueError("Especialidad inválida.")

        veterinario.set_telefono(nuevo_telefono)
        veterinario.set_especialidad(nueva_especialidad)

    def listar_veterinarios(self) -> None:
        if not self._veterinarios:
            print("No hay veterinarios registrados.")
            return

        for veterinario in self._veterinarios:
            print("------------------")
            veterinario.mostrar_info()

    def modificar_consultorio(self, numero: int, nueva_descripcion: str) -> None:
        consultorio = self._buscar_consultorio_por_numero(numero)

        if consultorio is None:
            raise ValueError("El consultorio no existe.")

        if nueva_descripcion.strip() == "":
            raise ValueError("Descripción inválida.")

        consultorio.set_descripcion(nueva_descripcion)

    def _buscar_consultorio_por_numero(self, numero: int) -> Consultorio:
        for consultorio in self._consultorios:
            if consultorio.get_numero() == numero:
                return consultorio
        return None

    def eliminar_consultorio(self, numero: int) -> None:
        consultorio = self._buscar_consultorio_por_numero(numero)

        if consultorio is None:
            raise ValueError("El consultorio no existe.")

        for turno in self._turnos:
            mismo_cons = turno.get_consultorio() == consultorio
            if mismo_cons and self._turno_activo_futuro(turno):
                raise ValueError(
                    "No se puede eliminar el consultorio porque tiene "
                    "turnos activos futuros asociados."
                )

        self._consultorios.remove(consultorio)

    def listar_consultorios(self) -> None:
        if not self._consultorios:
            print("No hay consultorios registrados.")
            return

        for consultorio in self._consultorios:
            print("------------------")
            consultorio.mostrar_info()
