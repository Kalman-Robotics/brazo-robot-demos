## Ejemplos que estan por testear

### `waypoints_json` — Ejecuta una secuencia de poses desde un archivo JSON

**Qué hace:** Lector genérico de secuencias: carga un JSON con lista de poses (angulares o cartesianas), cada una con su etiqueta, velocidad y tipo de movimiento, y las ejecuta en orden con una pausa configurable entre cada una. Útil para prototipar rutas sin tocar código.

**Con el archivo por defecto:**

```bash
python3 waypoints_json.py
```

**Con un archivo propio:**

```bash
python3 waypoints_json.py mi_secuencia.json
```

**Formato del JSON:**

```json
[
  {"flag": 0, "pose": [J1, J2, J3, J4, J5, J6], "speed": 10, "label": "home"},
  {"flag": 1, "pose": [X, Y, Z, RX, RY, RZ],    "speed": 20, "label": "punto_1"}
]
```

> `flag: 0` usa `send_angles`, `flag: 1` usa `send_coords`.

**Qué usa:**
- `send_angles(pose, speed)` — para poses con `flag: 0`
- `send_coords(pose, speed)` — para poses con `flag: 1`

**Parámetros** (al inicio del script): `ARCHIVO_DEFAULT` (JSON por defecto) · `PAUSA_ENTRE_POSES` (segundos de espera entre poses)

**Código:** [python/3 Programación y control/waypoints_json.py](python/3%20Programaci%C3%B3n%20y%20control/waypoints_json.py)

---

### `contador_objetos` — Recoge y cuenta objetos de una bandeja

**Qué hace:** El robot recoge objetos de una bandeja uno a uno, verifica con el gripper si hay objeto agarrado (estado `2`), los deposita en la zona de descarga y lleva un conteo acumulado que muestra cada `INTERVALO_DISPLAY` segundos. Se detiene al alcanzar `N_MAX_OBJETOS` o cuando la bandeja lleva `MAX_INTENTOS_VACIADA` intentos fallidos consecutivos.

```bash
python3 contador_objetos.py
```

> Este demo requiere objetos físicos en la bandeja. Consulta [README_testeo.md](README_testeo.md) para el flujo completo.

**Qué usa:**
- `send_angles(pose, speed)` — mueve a bandeja y zona de descarga
- `gripper_close()` / `gripper_open()` — intento de agarre
- `get_gripper_status()` — confirma objeto agarrado (estado `2`) o bandeja vacía
- `go_home()` — regresa al finalizar

**Parámetros** (al inicio del script): `POSE_BANDEJA_APPROACH`, `POSE_BANDEJA` · `POSE_DESCARGA_APPROACH`, `POSES_DESCARGA` · `N_MAX_OBJETOS` (límite de objetos) · `MAX_INTENTOS_VACIADA` (intentos fallidos antes de detener) · `INTERVALO_DISPLAY` · `SPEED`, `SPEED_PICK`, `ESPERA_GRIPPER`

**Código:** [python/4 Aplicaciones temáticas/contador_objetos.py](python/4%20Aplicaciones%20tem%C3%A1ticas/contador_objetos.py)
---

### `dibujo_svg` — Dibuja un archivo SVG en el plano

Este demo tiene pasos adicionales de verificación antes de mover el robot. Se recomienda ejecutar primero con `--preview` para confirmar la escala y la posición del dibujo antes de lanzar los movimientos reales.

**Vista previa (sin mover el robot):**

```bash
python3 dibujo_svg.py --preview
```

**Ejecución completa:**

```bash
python3 dibujo_svg.py
```

**Qué hace:** Carga un archivo SVG, extrae sus trazos, los escala y centra en el área de trabajo del robot, y los ejecuta como movimientos reales (pluma arriba o abajo según si el trazo es continuo o hay un salto). Con `--preview` genera solo la imagen sin mover el robot.

**Qué usa:**
- `send_coords(pose, speed)` — mueve el extremo a cada punto del trazo
- `set_fresh_mode(True/False)` — envío en ráfaga sin esperar entre puntos intermedios
- `gripper_close()` / `gripper_open()` — baja y sube la pluma entre trazos
- `go_home()` — regresa al finalizar

**Parámetros** (al inicio del script): `ANCHO_DIBUJO`, `ALTO_DIBUJO` (área máxima en mm) · `ORIGEN_X`, `ORIGEN_Y`, `PLANO_Z`, `Z_LEVANTE` (plano de trabajo) · `RESOLUCION` (muestreo de trazos) · `SPEED`, `SPEED_DRAW`

**Código:** [python/1 Movimiento y trayectorias/dibujo_svg.py](python/1%20Movimiento%20y%20trayectorias/dibujo_svg.py)

---
