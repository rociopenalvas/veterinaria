import json
import os


class MascotaDAO:

    def guardar(self, mascotas, path):

        # Crea el directorio si no existe.
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = []

        for m in mascotas:
            data.append({
                "nombre": m.get_nombre(),
                "especie": m._especie,
                "edad": m._edad,
                "raza": m.get_raza(),
                "dni_dueno": m.get_dueno().get_dni()
            })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def cargar(self, path, clinica):
        with open(path, "r") as f:
            data = json.load(f)

        for m in data:
            clinica.registrar_mascota(
                m["nombre"],
                m["especie"],
                m["edad"],
                m["raza"],
                m["dni_dueno"]
            )
