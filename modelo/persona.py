from abc import ABC, abstractmethod


class Persona(ABC):
    """Clase base abstracta para personas del sistema."""

    def __init__(self, dni: int, nombre: str, telefono: str):
        self._dni = dni
        self._nombre = nombre
        self._telefono = telefono

    def get_dni(self) -> int:
        return self._dni

    def get_nombre(self) -> str:
        return self._nombre

    def get_telefono(self) -> str:
        return self._telefono

    @abstractmethod
    def mostrar_info(self) -> None:
        """Muestra información de la persona en consola."""