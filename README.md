# Brazo Robot Demos

Scripts Python de demostración para el Brazo Robot myCobot Pro 450. Diseñados para ejecutarse desde tu laptop conectada al robot del laboratorio remoto.

## Prerrequisitos

- Python 3.8 o superior
- Conectado al laboratorio remoto (Husarnet activo, acceso al robot)

## Inicio rápido

### 1. Instalar la librería del robot

```bash
pip install --upgrade kalman-robot-arm
```

### 2. Clonar el repositorio

```bash
git clone https://github.com/Kalman-Robotics/brazo-robot-demos.git
cd brazo-robot-demos
```

### 3. Ejecutar un demo

```bash
python3 "python/1 Movimiento y trayectorias/geometrias_3d.py"
```

> Algunos scripts tienen poses marcadas con `TODO` pendientes de calibración. Mostrarán un aviso y saldrán sin mover el robot.

## Demos disponibles

### Movimiento y trayectorias

```bash
python3 "python/1 Movimiento y trayectorias/geometrias_3d.py"   # cuadrado, círculo y triángulo en el aire
python3 "python/1 Movimiento y trayectorias/escritura_K.py"     # escribe la letra K con un marcador
python3 "python/1 Movimiento y trayectorias/dibujo_svg.py" --preview   # previsualizar SVG sin mover el robot
python3 "python/1 Movimiento y trayectorias/dibujo_svg.py"             # dibujar SVG en el plano
python3 "python/1 Movimiento y trayectorias/reach_envelope.py"  # mapa 3D del workspace real
```

### Pick & Place

```bash
python3 "python/2 Pick & Place/pick_place_basico.py"    # recoge objeto A y lo deposita en B
python3 "python/2 Pick & Place/apilado.py"             # apila objetos incrementando el Z
python3 "python/2 Pick & Place/distribucion_1_a_N.py"  # distribuye a N posiciones en secuencia
```

### Interacción y demostración visual

```bash
python3 "python/3 Interacción y demostración visual/saludo.py"   # secuencia de saludo (wave)
```

### Programación y control

```bash
python3 "python/4 Programación y control/waypoints_json.py"              # ejecuta secuencia desde JSON
python3 "python/4 Programación y control/waypoints_json.py mi_ruta.json" # con archivo propio
python3 "python/4 Programación y control/pid_posicion.py"               # lazo cerrado proporcional en J1
```

### Aplicaciones temáticas

```bash
python3 "python/5 Aplicaciones temáticas/barman.py"          # secuencia de servir un vaso
python3 "python/5 Aplicaciones temáticas/contador_objetos.py" # cuenta objetos de una bandeja
```
