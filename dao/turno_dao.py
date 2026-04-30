import json
from datetime import datetime
import os


class TurnoDAO:

    def guardar(self, turnos, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = []

        for t in turnos:
            data.append({
                "nombre_mascota": t.get_mascota().get_nombre(),
                "dni_dueno": t.get_mascota().get_dueno().get_dni(),
                "matricula": t.get_veterinario().get_matricula(),
                "consultorio": t.get_consultorio().get_numero(),
                "fecha": t.get_fecha_hora().isoformat(),
                "estado": t.get_estado()
            })

        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def cargar(self, path, clinica):
        with open(path, "r") as f:
            data = json.load(f)

        for t in data:
            fecha = datetime.fromisoformat(t["fecha"])

            clinica.agendar_turno(
                t["nombre_mascota"],
                t["dni_dueno"],
                t["matricula"],
                t["consultorio"],
                fecha
            )

            # manejar estado
            if t["estado"] == "Cancelado":
                clinica._turnos[-1].cancelar()