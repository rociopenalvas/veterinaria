import json
import os


class VeterinarioDAO:
    """Persistencia de veterinarios en formato JSON."""

    def guardar(self, veterinarios, path):
        """Guarda la colección de veterinarios en disco."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = []

        for v in veterinarios:
            data.append({
                "dni": v.get_dni(),
                "nombre": v.get_nombre(),
                "telefono": v.get_telefono(),
                "matricula": v.get_matricula(),
                "especialidad": v.get_especialidad()
            })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def cargar(self, path, clinica):
        """Carga veterinarios desde disco y los registra en la clínica."""
        with open(path, "r") as f:
            data = json.load(f)

        for v in data:
            clinica.registrar_veterinario(
                v["dni"],
                v["nombre"],
                v["telefono"],
                v["matricula"],
                v["especialidad"]
            )