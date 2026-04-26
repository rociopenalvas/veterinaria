from animal import Animal
from dueno import Dueno


class Mascota(Animal):
    def __init__(self, especie: str, edad: int, nombre: str, raza: str, dueno: Dueno):
        super().__init__(especie, edad)
        self._nombre = nombre
        self._raza = raza
        self._dueno = dueno

    def get_nombre(self) -> str:
        return self._nombre

    def get_raza(self) -> str:
        return self._raza

    def get_dueno(self) -> Dueno:
        return self._dueno
    
    def set_edad(self, edad: int):
        self._edad = edad

    def mostrar_info(self):
        print(f"  Nombre: {self._nombre}")
        print(f"  Especie: {self._especie}")
        print(f"  Edad: {self._edad} años")
        print(f"  Raza: {self._raza}")
        print(f"  Dueño: {self._dueno.get_nombre()}")