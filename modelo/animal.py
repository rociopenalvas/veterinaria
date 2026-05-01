from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, especie: str, edad: int):
        self._especie = especie
        self._edad = edad

    def get_especie(self) -> str:
        return self._especie

    def get_edad(self) -> int:
        return self._edad

    @abstractmethod
    def mostrar_info(self):
        pass