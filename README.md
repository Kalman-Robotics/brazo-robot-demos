# Demos Python — Brazo Robot myCobot Pro 450

Scripts de demostración usando `kalman_robot_arm`. Cada script deja las poses
vacías o con valores de placeholder — el CEO en el laboratorio completa las
posiciones con los valores reales del robot físico.

Convención de placeholder: `TODO_POSE = None  # completar con [J1..J6] o [x,y,z,rx,ry,rz]`

---

## Movimiento y trayectorias

### `geometrias_3d.py`
Traza figuras geométricas en el espacio cartesiano (cuadrado, círculo, triángulo)
usando `send_coords` en secuencia. Al terminar genera un gráfico 3D con `matplotlib`.

- Requiere: `matplotlib`

### `escritura_K.py`
El extremo sigue los trazos de la letra **K** en un plano cartesiano fijo.
Diseñado para usarse con un marcador sujeto al gripper.

### `dibujo_svg.py`
Carga un archivo SVG y convierte cada path en movimientos cartesianos.
Pipeline: SVG → `svgpathtools` → muestreo → escalado → `send_coords`.

- Requiere: `svgpathtools`, `matplotlib`
- Uso: `python dibujo_svg.py cat.svg` o `python dibujo_svg.py --preview`
- Assets incluidos: `cat.svg`, `seven.svg`

### `reach_envelope.py`
Visita combinaciones de ángulos articulares y genera una nube de puntos 3D del workspace real.

- Output: `workspace_points.csv` + gráfico 3D

---

## Pick & Place

### `pick_place_basico.py`
Recoge un objeto de la posición A y lo deposita en B. Verifica agarre con `get_gripper_status()==2`.

### `apilado.py`
Recoge desde posición fija e incrementa el Z de depósito en cada ciclo.

### `distribucion_1_a_N.py`
Recoge desde un punto fijo y distribuye a N posiciones de depósito en secuencia.

---

## Interacción y demostración visual

### `saludo.py`
Secuencia de ángulos que simula un movimiento de saludo (wave). LED verde durante el saludo.

---

## Programación y control

### `waypoints_json.py`
Lee poses desde un archivo `.json` y las recorre en orden.
Incluye `waypoints_ejemplo.json` como plantilla.

### `pid_posicion.py`
Bucle de control proporcional sobre J1. Demo educativa de lazo cerrado en Python puro.

---

## Aplicaciones temáticas

### `barman.py`
Secuencia coreográfica que simula agarrar un vaso, trasladarlo y "servirlo".

### `contador_objetos.py`
Recoge objetos de una bandeja y muestra el conteo acumulado en consola.

---

## Estado de implementación

| Script | Estructura | Poses | Listo |
|---|---|---|---|
| `geometrias_3d.py` | ✅ | ✅ | ✅ |
| `escritura_K.py` | ✅ | ✅ | ✅ |
| `dibujo_svg.py` | ✅ | ✅ | ✅ |
| `reach_envelope.py` | ✅ | ✅ | ✅ |
| `pick_place_basico.py` | ✅ | ✅ | ✅ |
| `apilado.py` | ✅ | ⬜ | ⬜ |
| `distribucion_1_a_N.py` | ✅ | ⬜ | ⬜ |
| `saludo.py` | ✅ | ⬜ | ⬜ |
| `waypoints_json.py` | ✅ | ✅ | ✅ |
| `pid_posicion.py` | ✅ | ✅ | ✅ |
| `barman.py` | ✅ | ⬜ | ⬜ |
| `contador_objetos.py` | ✅ | ✅ | ✅ |
