from datetime import datetime

from modelo.mascota import Mascota
from modelo.veterinario import Veterinario
from modelo.consultorio import Consultorio

class Turno:
    """
    Representa un turno veterinario.
    Conecta mascota, veterinario y consultorio con fecha/hora.
    """
    #Contador para enumerar e identificar los turnos
    _contador_id = 1

    def __init__(
        self,
        mascota: Mascota,
        veterinario: Veterinario,
        fecha_hora: datetime,
        consultorio: Consultorio,
        *,
        id_existente: int | None = None,
        estado: str | None = None,
        validar_fecha_futura: bool = True,
    ):
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
    def sincronizar_contador_tras_carga(cls, turnos: list) -> None:
        """Evita colisiones de id al crear turnos nuevos después de cargar desde disco."""
        if turnos:
            cls._contador_id = max(t.get_id() for t in turnos) + 1

    def get_mascota(self) -> Mascota:
        return self._mascota

    def get_veterinario(self) -> Veterinario:
        return self._veterinario

    def get_fecha_hora(self) -> datetime:
        return self._fecha_hora

    def get_consultorio(self) -> Consultorio:
        return self._consultorio

    def get_estado(self) -> str:
        return self._estado

    def get_id(self) -> int:
        return self._id

    # Métodos principales
    def cancelar(self):
        self._estado = "Cancelado"

    def modificar_fecha(self, nueva_fecha_hora: datetime):
        """
        Modifica la fecha y hora del turno.
        Verifica que sea futuro.
        """
        if nueva_fecha_hora <= datetime.now():
            raise ValueError("La nueva fecha debe ser futura.")
        self._fecha_hora = nueva_fecha_hora

    def mostrar_info(self):
        print(f"  Mascota: {self._mascota.get_nombre()}")
        print(f"  Dueño: {self._mascota.get_dueno().get_nombre()} DNI: {self._mascota.get_dueno().get_dni()}")
        print(f"  Veterinario: {self._veterinario.get_nombre()} Matrícula: {self._veterinario.get_matricula()}")
        print(f"  Fecha y hora: {self._fecha_hora}")
        print(f"  Consultorio: {self._consultorio.get_numero()}")
        print(f"  Estado: {self._estado}")