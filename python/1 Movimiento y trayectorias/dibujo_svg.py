"""
Demo: Dibujo de imagen SVG

Carga un archivo SVG, extrae los trazos y los convierte en movimientos
cartesianos del robot. Análogo a GCode:

  G0 X Y   (movimiento rápido, pluma arriba)  →  send_coords Z=Z_LEVANTE
  G1 X Y F (movimiento lineal, pluma abajo)   →  send_coords Z=PLANO_Z

Requiere:
    pip install svgpathtools

Uso:
    python dibujo_svg.py              → usa el SVG por defecto (cat.svg)
    python dibujo_svg.py figura.svg   → SVG personalizado
    python dibujo_svg.py --preview    → solo genera el gráfico, sin mover el robot
"""

import sys
from pathlib import Path
from time import sleep

try:
    from svgpathtools import svg2paths
except ImportError:
    print("\n  Falta svgpathtools:")
    print("  pip install svgpathtools\n")
    sys.exit(1)

from kalman_robot_arm import KalmanRobotArm

ORIGEN_X  = 280
ORIGEN_Y  = -85
PLANO_Z   = 400
Z_LEVANTE = 415
PLANO_RX  = -180
PLANO_RY  = 0
PLANO_RZ  = -90

SVG_DEFAULT  = Path(__file__).parent / "seven.svg"
ANCHO_DIBUJO = 100
ALTO_DIBUJO  = 100
RESOLUCION   = 180
SPEED        = 30
SPEED_DRAW   = 50

args       = [a for a in sys.argv[1:] if not a.startswith("--")]
flags      = [a for a in sys.argv[1:] if a.startswith("--")]
solo_preview = "--preview" in flags

svg_file = Path(args[0]) if args else SVG_DEFAULT

if not svg_file.exists():
    print(f"\n  Archivo no encontrado: {svg_file}")
    sys.exit(1)

paths, _ = svg2paths(str(svg_file))
print(f"  Procesando {len(paths)} paths SVG...", flush=True)

trazos_raw = []
for idx, path in enumerate(paths):
    try:
        length = path.length(error=1e-2)
    except Exception:
        continue
    if length < 1:
        continue
    n = max(2, int(length / RESOLUCION))
    puntos = [path.point(i / n) for i in range(n + 1)]
    trazos_raw.append([(p.real, p.imag) for p in puntos])
    print(f"  {idx + 1}/{len(paths)} paths...", end="\r", flush=True)

print()

if not trazos_raw:
    print("  El SVG no contiene paths válidos.")
    sys.exit(1)

all_x = [x for t in trazos_raw for x, y in t]
all_y = [y for t in trazos_raw for x, y in t]

svg_w = max(all_x) - min(all_x)
svg_h = max(all_y) - min(all_y)

escala = min(ANCHO_DIBUJO / svg_w, ALTO_DIBUJO / svg_h)
offset_x = ORIGEN_X - (max(all_x) + min(all_x)) / 2 * escala
offset_y = ORIGEN_Y - (max(all_y) + min(all_y)) / 2 * escala
_y_flip = (max(all_y) + min(all_y)) * escala

def svg_to_robot(sx, sy):
    rx = sx * escala + offset_x
    ry = -sy * escala + offset_y + _y_flip
    return rx, ry

def _dist(a, b):
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2) ** 0.5

UMBRAL_SALTO_MM = 3.0

trazos = []
for trazo_raw in trazos_raw:
    pts = [svg_to_robot(sx, sy) for sx, sy in trazo_raw]
    segmento = [pts[0]]
    for pt in pts[1:]:
        if _dist(segmento[-1], pt) > UMBRAL_SALTO_MM:
            if len(segmento) >= 2:
                trazos.append(segmento)
            segmento = [pt]
        else:
            segmento.append(pt)
    if len(segmento) >= 2:
        trazos.append(segmento)

n_puntos   = sum(len(t) for t in trazos)
ancho_real = svg_w * escala
alto_real  = svg_h * escala
seg_est = n_puntos * 0.35 + len(trazos) * 0.5

print(f"\n  SVG: {svg_file.name}")
print(f"  Trazos: {len(trazos)}   |   Puntos: {n_puntos}")
print(f"  Tamaño en robot: {ancho_real:.0f} × {alto_real:.0f} mm")
print(f"  Tiempo estimado: ~{seg_est / 60:.1f} min\n")

SALIDA_PREVIEW = Path(__file__).parent / (svg_file.stem + "_preview.png")

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 6))
    for trazo in trazos:
        xs = [p[0] for p in trazo]
        ys = [p[1] for p in trazo]
        ax.plot(xs, ys, "-", linewidth=0.8, color="black")

    ax.set_xlabel("X robot (mm)")
    ax.set_ylabel("Y robot (mm)")
    ax.set_title(f"{svg_file.stem} — {len(trazos)} trazos")
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(SALIDA_PREVIEW, dpi=150)
    print(f"  Preview guardado: {SALIDA_PREVIEW.name}")

except ImportError:
    print("  pip install matplotlib  para preview")

if solo_preview:
    print("  Modo --preview: robot no ejecutado.")
    sys.exit(0)

def coord(rx, ry, z):
    return [rx, ry, z, PLANO_RX, PLANO_RY, PLANO_RZ]

robot = KalmanRobotArm()
robot.set_color(0, 0, 255)
robot.gripper_close()
print("  Iniciando dibujo...\n")

for i, trazo in enumerate(trazos, 1):
    rx0, ry0 = trazo[0]

    robot.set_color(255, 165, 0)
    robot.send_coords(coord(rx0, ry0, Z_LEVANTE), SPEED)
    robot.wait_until_stopped()

    robot.send_coords(coord(rx0, ry0, PLANO_Z), SPEED_DRAW)
    robot.wait_until_stopped()
    sleep(0.05)

    robot.set_color(255, 255, 255)
    robot.set_fresh_mode(True)
    for rx, ry in trazo[1:]:
        robot.send_coords(coord(rx, ry, PLANO_Z), SPEED_DRAW)
    robot.set_fresh_mode(False)

    rx_fin, ry_fin = trazo[-1]
    robot.send_coords(coord(rx_fin, ry_fin, Z_LEVANTE), SPEED_DRAW)
    robot.wait_until_stopped()

    print(f"  Trazo {i:3d}/{len(trazos)}", end="\r")

robot.set_color(0, 255, 0)
print(f"\n  Dibujo completado — {len(trazos)} trazos.")

robot.go_home()
robot.wait_until_stopped()
robot.gripper_open()
robot.set_color(0, 0, 0)
