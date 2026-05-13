from abc import ABC, abstractmethod


class Animal(ABC):

    def __init__(self, especie: str, edad: int, raza: str):
        self._especie = especie
        self._edad = edad
        self._raza = raza

    def get_especie(self) -> str:
        return self._especie

    def get_edad(self) -> int:
        return self._edad

    def get_raza(self) -> str:
        return self._raza

    @abstractmethod
    def mostrar_info(self) -> None:
        """Muestra información del animal en consola."""
        pass
