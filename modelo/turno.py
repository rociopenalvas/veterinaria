from datetime import datetime, timedelta
from typing import Optional

from modelo.mascota import Mascota
from modelo.veterinario import Veterinario
from modelo.consultorio import Consultorio


class Turno:
    """
    Conecta una mascota, un veterinario y un consultorio con una fecha/hora.
    Cada turno ocupa un bloque fijo desde esa hora (ver DURACION_MINUTOS).
    """
    DURACION_MINUTOS = 30
    _contador_id = 1

    def __init__(
        self,
        mascota: Mascota,
        veterinario: Veterinario,
        fecha_hora: datetime,
        consultorio: Consultorio,
        *,
        id_existente: Optional[int] = None,
        estado: Optional[str] = None,
        validar_fecha_futura: bool = True,
    ):
        self._validar_bloque_horario(fecha_hora)
        if validar_fecha_futura and fecha_hora <= datetime.now():
            raise ValueError("La fecha y hora del turno debe ser futura.")
        self._mascota = mascota
        self._veterinario = veterinario
        self._fecha_hora = fecha_hora
        self._consultorio = consultorio
        self._estado = estado if estado is not None else "Activo"
        if id_existente is not None:
            self._id = id_existente
        else:
            self._id = Turno._contador_id
            Turno._contador_id += 1

    @classmethod
    def _validar_bloque_horario(cls, fecha_hora: datetime) -> None:
        if not (
            fecha_hora.minute == 0
            or fecha_hora.minute == 15
            or fecha_hora.minute == 30
            or fecha_hora.minute == 45
        ) or fecha_hora.second != 0:
            raise ValueError("El turno debe comenzar en minuto 00, 15, 30 o 45.")

    @classmethod
    def sincronizar_contador_tras_carga(cls, turnos: list) -> None:
        # Sin esto, al cargar JSON los ids nuevos podrían repetir los viejos.
        if turnos:
            cls._contador_id = max(t.get_id() for t in turnos) + 1

    def get_mascota(self) -> Mascota:
        return self._mascota

    def get_veterinario(self) -> Veterinario:
        return self._veterinario

    def get_fecha_hora(self) -> datetime:
        return self._fecha_hora

    def get_fecha_fin(self) -> datetime:
        return self._fecha_hora + timedelta(minutes=self.DURACION_MINUTOS)

    def get_consultorio(self) -> Consultorio:
        return self._consultorio

    def get_estado(self) -> str:
        return self._estado

    def get_id(self) -> int:
        return self._id

    def cancelar(self) -> None:
        self._estado = "Cancelado"

    def modificar_fecha(self, nueva_fecha_hora: datetime):
        """
        Modifica la fecha y hora, verificando que sea futura y que sea un bloque válido.
        """
        if nueva_fecha_hora <= datetime.now():
            raise ValueError("La nueva fecha debe ser futura.")
        self._validar_bloque_horario(nueva_fecha_hora)
        self._fecha_hora = nueva_fecha_hora

    def mostrar_info(self) -> None:
        print(f"  Mascota: {self._mascota.get_nombre()}")
        print(f"  Dueño: {self._mascota.get_dueno().get_nombre()} DNI: {self._mascota.get_dueno().get_dni()}")
        print(f"  Veterinario: {self._veterinario.get_nombre()} Matrícula: {self._veterinario.get_matricula()}")
        print(f"  Inicio: {self._fecha_hora}  Fin estimado: {self.get_fecha_fin()}")
        print(f"  Consultorio: {self._consultorio.get_numero()}")
        print(f"  Estado: {self._estado}")
