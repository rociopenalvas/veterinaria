import json
from datetime import datetime
import os

from modelo.turno import Turno


class TurnoDAO:

    def guardar(self, turnos, path):

        # Crea el directorio si no existe.
        os.makedirs(os.path.dirname(path), exist_ok=True)

        data = []

        for t in turnos:
            data.append({
                "id": t.get_id(),
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

            clinica.restaurar_turno(
                t["nombre_mascota"],
                t["dni_dueno"],
                t["matricula"],
                t["consultorio"],
                fecha,
                t["id"],
                t["estado"],
            )

        Turno.sincronizar_contador_tras_carga(clinica._turnos)
