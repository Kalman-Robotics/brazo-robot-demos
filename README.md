# Brazo Robot Demos

Scripts Python de demostración para el Brazo Robot myCobot Pro 450. Diseñados para ejecutarse desde tu laptop conectada al robot del laboratorio remoto.

## Prerrequisitos

- Python 3.8 o superior
- Conectado al laboratorio remoto (Husarnet activo, acceso al robot)

## Inicio rápido

### 1. Instalar las librerías

```bash
pip install --upgrade kalman-robot-arm
pip install matplotlib
```

### 2. Clonar el repositorio

```bash
git clone https://github.com/Kalman-Robotics/brazo-robot-demos.git
cd brazo-robot-demos
```

### 3. Ejecutar un demo

```bash
cd "python/1 Movimiento y trayectorias"
python3 geometrias_3d.py
```

> Algunos scripts tienen poses marcadas con `TODO` pendientes de calibración. Mostrarán un aviso y saldrán sin mover el robot.

## Demos disponibles

### Movimiento y trayectorias

```bash
cd "python/1 Movimiento y trayectorias"
```

| Script | Descripción |
|---|---|
| `python3 geometrias_3d.py` | Traza un cuadrado, círculo y triángulo en el espacio cartesiano |
| `python3 escritura_K.py` | Escribe la letra K en un plano fijo con un marcador |
| `python3 dibujo_svg.py --preview` | Previsualiza el SVG sin mover el robot (el archivo SVG se especifíca dentro del script) |
| `python3 dibujo_svg.py` | Dibuja un SVG en el plano |
| `python3 reach_envelope.py` | Genera una nube de puntos 3D del workspace real |

### Pick & Place

```bash
cd "python/2 Pick & Place"
```

| Script | Descripción |
|---|---|
| `python3 pick_place_basico.py` | Recoge un objeto de la posición A y lo deposita en B |
| `python3 apilado.py` | Apila objetos incrementando el Z de depósito por capa |
| `python3 distribucion_1_a_N.py` | Distribuye piezas a N posiciones en secuencia |

### Programación y control

```bash
cd "python/3 Programación y control"
```

| Script | Descripción |
|---|---|
| `python3 waypoints_json.py` | Ejecuta secuencia de poses desde `waypoints_ejemplo.json` |
| `python3 waypoints_json.py mi_ruta.json` | Usa un archivo JSON propio |
| `python3 pid_posicion.py` | Lazo cerrado proporcional sobre J1 — demo educativa de control |

### Aplicaciones temáticas

```bash
cd "python/4 Aplicaciones temáticas"
```

| Script | Descripción |
|---|---|
| `python3 barman.py` | Secuencia coreográfica de agarrar y servir un vaso |
| `python3 contador_objetos.py` | Recoge objetos de una bandeja y muestra conteo acumulado |
