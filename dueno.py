from persona import Persona


class Dueno(Persona):
    def __init__(self, dni: int, nombre: str, telefono: str, direccion: str):
        super().__init__(dni, nombre, telefono)
        self._direccion = direccion

    def get_direccion(self) -> str:
        return self._direccion

    def mostrar_info(self):
        print(f" DNI: {self._dni}")
        print(f"  Nombre: {self._nombre}")
        print(f"  Teléfono: {self._telefono}")
        print(f"  Dirección: {self._direccion}")

    def set_telefono(self, telefono: str):
        self._telefono = telefono

    def set_direccion(self, direccion: str):
        self._direccion = direccion