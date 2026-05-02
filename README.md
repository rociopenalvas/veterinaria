# Sistema de Turnos Veterinaria

Trabajo practico de Programacion Orientada a Objetos (Python).

## Requisitos

- Python 3.10 o superior

## Como ejecutar

Desde la carpeta del proyecto:

```bash
py main.py
```

## Como ejecutar tests

```bash
py -m pytest test/ -q
```

## Funcionalidades principales

- Registro y gestion de:
  - Duenos
  - Mascotas
  - Veterinarios
  - Consultorios
  - Turnos
- Agenda de turnos:
  - Alta, modificacion y cancelacion
  - Consultas por fecha, veterinario, mascota y dueno
- Persistencia en archivos JSON (`data/`).

## Reglas de negocio importantes

- Los turnos tienen duracion fija de 30 minutos.
- Los turnos solo pueden iniciar en minutos `00`, `15`, `30` o `45`.
- No se permiten superposiciones de turnos para:
  - El mismo veterinario
  - El mismo consultorio
  - La misma mascota
- Se permite eliminar mascota, veterinario o consultorio solo si no tienen turnos activos futuros asociados.

## Estructura general

- `main.py`: punto de entrada.
- `menu.py`: interfaz por consola.
- `clinica.py`: logica principal del sistema.
- `modelo/`: clases del dominio.
- `dao/`: guardado y carga en JSON.
- `test/`: pruebas unitarias e integracion.
