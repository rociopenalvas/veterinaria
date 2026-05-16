# Sistema de turnos — veterinaria

Trabajo práctico de Programación Orientada a Objetos, hecho en Python.

## Requisitos

- Python **3.9 o superior** (con versiones más nuevas también debería andar bien).

## Cómo ejecutarlo

Desde la carpeta del proyecto:

```bash
py main.py
```

## Cómo correr los tests

```bash
py -m unittest discover -s test -p "test_*.py" -v
```

## Qué hace el sistema

- Registro y gestión de dueños, mascotas, veterinarios y consultorios.
- Turnos: alta, modificación, cancelación y listado (pasados/futuros).
- Consultas de turnos por fecha, veterinario, mascota y dueño.
- Los datos se guardan en archivos JSON dentro de la carpeta `data/`.

## Reglas de negocio que tiene en cuenta

- Los turnos duran 30 minutos (fijo).
- Solo pueden empezar en minutos `00`, `15`, `30` o `45`.
- No puede haber turnos que se pisen para el mismo veterinario, el mismo consultorio o la misma mascota.
- Solo se puede borrar una mascota, un veterinario o un consultorio si no tienen turnos activos a futuro. 
- Solo se puede borrar un Dueño si no tiene mascotas en el sistema.

## Organización del código

- `main.py`: arranca la aplicación.
- `menu.py`: menús por consola.
- `clinica.py`: donde está la lógica principal.
- `modelo/`: las clases del dominio.
- `dao/`: lectura y escritura en JSON.
- `test/`: pruebas unitarias y prueba de integración.
