import json
import os


class ConsultorioDAO:

    def guardar(self, consultorios, path):

        # Crea el directorio si no existe.
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = []

        for c in consultorios:
            data.append({
                "numero": c.get_numero(),
                "descripcion": c.get_descripcion()
            })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def cargar(self, path, clinica):
        with open(path, "r") as f:
            data = json.load(f)

        for c in data:
            clinica.registrar_consultorio(
                c["numero"],
                c["descripcion"]
            )
