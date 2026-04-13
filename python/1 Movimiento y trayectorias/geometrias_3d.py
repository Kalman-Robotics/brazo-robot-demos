"""
Demo: Dibujo de figuras geométricas en el aire

Traza un cuadrado, círculo y triángulo en el espacio cartesiano.
El LED cambia de color por figura.
Al terminar genera un gráfico 3D con matplotlib comparando
la trayectoria teórica vs la real (registrada con get_coords()).

Uso:
    python geometrias_3d.py
"""

import math
from pathlib import Path
from time import sleep
from kalman_robot_arm import KalmanRobotArm

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

ANGLES_INICIO  = [0.02, -19.24, -110.78, 46.33, 0.01, -0.01]

PLANO_Z  = 350    # [mm]
PLANO_RX = -180   # [°]
PLANO_RY = 0      # [°]
PLANO_RZ = -90    # [°]

CENTRO_X = 280    # [mm]
CENTRO_Y = -85    # [mm]

LADO_CUADRADO  = 120   # [mm]
RADIO_CIRCULO  = 80    # [mm]
LADO_TRIANGULO = 140   # [mm]

SPEED            = 40
N_PUNTOS_CIRCULO = 18

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def coord(x, y):
    return [x, y, PLANO_Z, PLANO_RX, PLANO_RY, PLANO_RZ]

def mover(robot, pose, registros):
    robot.send_coords(pose, SPEED)
    robot.wait_until_stopped(timeout=15)
    c = robot.get_coords()
    if isinstance(c, list) and len(c) == 6:
        registros.append(c)

def puntos_cuadrado(cx, cy, lado):
    h = lado / 2
    return [
        coord(cx - h, cy - h),
        coord(cx + h, cy - h),
        coord(cx + h, cy + h),
        coord(cx - h, cy + h),
        coord(cx - h, cy - h),
    ]

def puntos_circulo(cx, cy, radio, n):
    return [
        coord(cx + radio * math.cos(2 * math.pi * i / n),
              cy + radio * math.sin(2 * math.pi * i / n))
        for i in range(n + 1)
    ]

def puntos_triangulo(cx, cy, lado):
    h = lado * math.sqrt(3) / 2
    return [
        coord(cx,            cy + 2 * h / 3),
        coord(cx - lado / 2, cy - h / 3),
        coord(cx + lado / 2, cy - h / 3),
        coord(cx,            cy + 2 * h / 3),
    ]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

robot = KalmanRobotArm()

robot.send_angles(ANGLES_INICIO, SPEED)
robot.wait_until_stopped()

figuras = [
    ("Cuadrado",  (255, 0,   0),   puntos_cuadrado(CENTRO_X, CENTRO_Y, LADO_CUADRADO)),
    ("Círculo",   (0,   255, 0),   puntos_circulo(CENTRO_X, CENTRO_Y, RADIO_CIRCULO, N_PUNTOS_CIRCULO)),
    ("Triángulo", (0,   0,   255), puntos_triangulo(CENTRO_X, CENTRO_Y, LADO_TRIANGULO)),
]

registros = {nombre: [] for nombre, _, _ in figuras}

robot.gripper_close()
for nombre, color, puntos in figuras:
    print(f"\n  → {nombre}")
    robot.set_color(*color)
    sleep(0.3)
    for pt in puntos:
        mover(robot, pt, registros[nombre])
robot.gripper_open()

robot.set_color(0, 255, 0)
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
print("\n  Figuras completadas.")

# ---------------------------------------------------------------------------
# Visualización
# ---------------------------------------------------------------------------

SALIDA = Path(__file__).parent / "geometrias_3d.png"

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import mpl_toolkits.mplot3d

    colores_plt = {"Cuadrado": "red", "Círculo": "green", "Triángulo": "blue"}

    try:
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection="3d")

        for nombre, _, pts_teoricos in figuras:
            ax.plot([p[0] for p in pts_teoricos],
                    [p[1] for p in pts_teoricos],
                    [p[2] for p in pts_teoricos],
                    "--", color=colores_plt[nombre], alpha=0.4, label=f"{nombre} (teórico)")
            ax.plot([p[0] for p in registros[nombre]],
                    [p[1] for p in registros[nombre]],
                    [p[2] for p in registros[nombre]],
                    "-o", color=colores_plt[nombre], markersize=3, label=f"{nombre} (real)")

        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.set_zlabel("Z (mm)")
        ax.set_title("Trayectorias — teórico vs real (3D)")
        ax.legend()

    except Exception:
        print("  3D no disponible — generando gráfico 2D (XY)")
        fig, ax = plt.subplots(figsize=(8, 6))

        for nombre, _, pts_teoricos in figuras:
            ax.plot([p[0] for p in pts_teoricos],
                    [p[1] for p in pts_teoricos],
                    "--", color=colores_plt[nombre], alpha=0.4, label=f"{nombre} (teórico)")
            ax.plot([p[0] for p in registros[nombre]],
                    [p[1] for p in registros[nombre]],
                    "-o", color=colores_plt[nombre], markersize=3, label=f"{nombre} (real)")

        ax.set_xlabel("X (mm)")
        ax.set_ylabel("Y (mm)")
        ax.set_title("Trayectorias — teórico vs real (XY)")
        ax.legend()
        ax.set_aspect("equal")

    plt.tight_layout()
    plt.savefig(SALIDA, dpi=150)
    plt.show()
    print(f"  Gráfico guardado: {SALIDA}")

except ImportError:
    print("  pip install matplotlib  para visualización")
