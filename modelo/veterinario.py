from modelo.persona import Persona


class Veterinario(Persona):
    """Representa a un veterinario de la clínica."""

    def __init__(self, dni: int, nombre: str, telefono: str, matricula: str, especialidad: str):
        super().__init__(dni, nombre, telefono)
        self._matricula = matricula
        self._especialidad = especialidad

    def get_matricula(self) -> str:
        return self._matricula

    def get_especialidad(self) -> str:
        return self._especialidad

    def mostrar_info(self) -> None:
        print(f" DNI: {self._dni}")
        print(f"  Nombre: {self._nombre}")
        print(f"  Teléfono: {self._telefono}")
        print(f" Matrícula: {self._matricula}")
        print(f"  Especialidad: {self._especialidad}")

    def set_telefono(self, telefono: str):
        self._telefono = telefono

    def set_especialidad(self, especialidad: str):
        self._especialidad = especialidad