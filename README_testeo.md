# Testeo y ejemplos — Brazo Robot Demos

Comandos para verificar que el entorno está correctamente instalado y probar los scripts. Empieza siempre por los tests sin robot.

---

## 1. Verificar instalación de librerías

```bash
python3 -c "import pymycobot; print('pymycobot OK')"
python3 -c "import matplotlib; print('matplotlib OK')"
python3 -c "import svgpathtools; print('svgpathtools OK')"
```

Si alguna falla:

```bash
pip install --upgrade kalman-robot-arm
pip install matplotlib svgpathtools
```

---

## 2. `dibujo_svg` — Flujo completo

Este demo requiere verificar el resultado visual antes de mover el robot. Sigue los pasos en orden.

### Paso 1 — Posicionarse en la carpeta

```bash
cd ~/brazo-robot-demos/python/1\ Movimiento\ y\ trayectorias
```

### Paso 2 — Previsualizar sin mover el robot

```bash
python3 dibujo_svg.py --preview
```

Debe abrirse una ventana matplotlib con la figura escalada al área de trabajo. Verifica que la forma se ve correcta y que no hay trazos fuera de los límites antes de continuar.

### Paso 3 — Ejecutar en el robot

Una vez que el preview se ve bien:

```bash
python3 dibujo_svg.py
```

### Usar un SVG propio

Copia tu archivo `.svg` en la misma carpeta y repite el flujo:

```bash
python3 dibujo_svg.py mi_figura.svg --preview
python3 dibujo_svg.py mi_figura.svg
```

> El SVG debe tener trazos vectoriales (`<path>`). Imágenes rasterizadas exportadas como `.svg` no funcionan — usa Inkscape y exporta como "SVG simple".

---

## 3. `contador_objetos` — Flujo completo

Este demo requiere objetos físicos colocados en la bandeja antes de ejecutarlo.

### Paso 1 — Preparar el escenario

Coloca entre 1 y `N_MAX_OBJETOS` objetos en la bandeja en la posición `POSE_BANDEJA`. El robot intentará recoger desde esa misma posición en cada ciclo.

### Paso 2 — Posicionarse en la carpeta

```bash
cd ~/brazo-robot-demos/python/4\ Aplicaciones\ temáticas
```

### Paso 3 — Ejecutar

```bash
python3 contador_objetos.py
```

El robot recoge un objeto, verifica con el gripper si lo agarró (estado `2`), lo deposita en la zona de descarga y muestra el conteo cada `INTERVALO_DISPLAY` segundos. Se detiene cuando alcanza `N_MAX_OBJETOS` o cuando hay `MAX_INTENTOS_VACIADA` intentos fallidos consecutivos (bandeja vacía).

> Si el gripper no detecta objeto (estado ≠ `2`), el robot lo cuenta como fallo y continúa con el siguiente intento. Ajusta `MAX_INTENTOS_VACIADA` en el script para controlar cuántos fallos consecutivos tolera antes de detenerse.

---

## 5. Ejemplos rápidos con robot conectado

> Asegúrate de que Husarnet está activo y el robot responde antes de continuar.

### Geometrías 3D

```bash
cd ~/brazo-robot-demos/python/1\ Movimiento\ y\ trayectorias
python3 geometrias_3d.py
```

El robot traza un cuadrado, un círculo y un triángulo. Al terminar se abre una gráfica comparando trayectoria teórica vs real.

### Escritura de la letra K

```bash
cd ~/brazo-robot-demos/python/1\ Movimiento\ y\ trayectorias
python3 escritura_K.py
```

### Workspace real

```bash
cd ~/brazo-robot-demos/python/1\ Movimiento\ y\ trayectorias
python3 reach_envelope.py
```

El robot barre posiciones articulares y guarda las coordenadas reales en un CSV. Al terminar muestra una nube de puntos 3D del espacio alcanzable.

### Pick & Place básico

```bash
cd ~/brazo-robot-demos/python/2\ Pick\ \&\ Place
python3 pick_place_basico.py
```

### Control proporcional J1

```bash
cd ~/brazo-robot-demos/python/3\ Programación\ y\ control
python3 pid_posicion.py
```

El terminal muestra en tiempo real la tabla del lazo de control hasta que converge.

### Waypoints desde JSON

```bash
cd ~/brazo-robot-demos/python/3\ Programación\ y\ control
python3 waypoints_json.py
```

---

## 6. Problemas comunes

| Síntoma | Causa probable | Solución |
|---|---|---|
| `ModuleNotFoundError: svgpathtools` | Librería no instalada | `pip install svgpathtools` |
| `ModuleNotFoundError: pymycobot` | kalman-robot-arm no instalado | `pip install --upgrade kalman-robot-arm` |
| El SVG aparece vacío en preview | SVG sin trazos `<path>` vectoriales | Exportar desde Inkscape como "SVG simple" |
| El robot no responde | Husarnet desconectado o robot apagado | Verificar conexión al laboratorio remoto |
| `Connection refused` al conectar | IP del robot incorrecta | Revisar la configuración en el script |
