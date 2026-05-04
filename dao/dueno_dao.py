import json
import os


class DuenoDAO:

    def guardar(self, duenos, path):

        # Crea el directorio si no existe.
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = []

        for d in duenos:
            data.append({
                "dni": d.get_dni(),
                "nombre": d.get_nombre(),
                "telefono": d.get_telefono(),
                "direccion": d.get_direccion()
            })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def cargar(self, path, clinica):
        with open(path, "r") as f:
            data = json.load(f)

        for d in data:
            clinica.registrar_dueno(
                d["dni"],
                d["nombre"],
                d["telefono"],
                d["direccion"]
            )
