class Consultorio:

    def __init__(self, numero: int, descripcion: str):
        self._numero = numero
        self._descripcion = descripcion

    def get_numero(self) -> int:
        return self._numero

    def get_descripcion(self) -> str:
        return self._descripcion

    def mostrar_info(self) -> None:
        print(f" Número: {self._numero}")
        print(f"  Descripción: {self._descripcion}")

    def set_descripcion(self, descripcion: str) -> None:
        self._descripcion = descripcion
