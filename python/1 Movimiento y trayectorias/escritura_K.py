"""
Demo: Escritura de la letra K en un plano cartesiano fijo

El extremo sigue los tres trazos de la letra K sujetando un marcador.
Los puntos se definen como offsets XY relativos a un origen configurable.

Parámetros a calibrar con el CEO:
  ORIGEN_X, ORIGEN_Y  — coordenada cartesiana del extremo inferior-izquierdo de la K
  PLANO_Z             — altura del plano de escritura
  Z_LEVANTE           — altura a la que se levanta la pluma entre trazos
  PLANO_RX/RY/RZ      — orientación del extremo

Uso:
    python escritura_K.py
"""

from pathlib import Path
from time import sleep
from kalman_robot_arm import KalmanRobotArm

# ---------------------------------------------------------------------------
# Parámetros del plano de escritura — CALIBRAR CON EL CEO
# ---------------------------------------------------------------------------

ORIGEN_X = 280
ORIGEN_Y = -85

PLANO_Z  = 400
Z_LEVANTE = 415

PLANO_RX = -180
PLANO_RY = 0
PLANO_RZ = -90

ALTO_K  = 100
ANCHO_K = 60

SPEED      = 20
SPEED_DRAW = 10

PENDIENTES = {
    "ORIGEN_X": ORIGEN_X,
    "ORIGEN_Y": ORIGEN_Y,
    "PLANO_Z":  PLANO_Z,
    "Z_LEVANTE": Z_LEVANTE,
    "PLANO_RX": PLANO_RX,
    "PLANO_RY": PLANO_RY,
    "PLANO_RZ": PLANO_RZ,
}
faltantes = [k for k, v in PENDIENTES.items() if v is None]
if faltantes:
    print(f"\n  ⚠  Parámetros pendientes: {faltantes}")
    print("  Calibrar con el CEO antes de ejecutar.\n")
    exit(0)

# ---------------------------------------------------------------------------
# Definición de trazos de la K
# ---------------------------------------------------------------------------

MID_Y = ALTO_K / 2

TRAZOS = [
    [(0, ALTO_K), (0, 0)],
    [(0, MID_Y), (ANCHO_K, ALTO_K)],
    [(0, MID_Y), (ANCHO_K, 0)],
]

def coord_escritura(dx, dy, z):
    return [ORIGEN_X + dx, ORIGEN_Y + dy, z, PLANO_RX, PLANO_RY, PLANO_RZ]

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

robot = KalmanRobotArm()
robot.set_color(0, 0, 255)
print("\n  Escritura K — iniciando\n")

primer_punto = TRAZOS[0][0]
robot.send_coords(coord_escritura(*primer_punto, Z_LEVANTE), SPEED)
robot.wait_until_stopped()
robot.gripper_close()

for i, trazo in enumerate(TRAZOS, start=1):
    print(f"  Trazo {i}/{len(TRAZOS)}")

    robot.set_color(255, 165, 0)
    robot.send_coords(coord_escritura(*trazo[0], Z_LEVANTE), SPEED)
    robot.wait_until_stopped()

    robot.send_coords(coord_escritura(*trazo[0], PLANO_Z), SPEED_DRAW)
    robot.wait_until_stopped()
    sleep(0.1)

    robot.set_color(255, 255, 255)
    for punto in trazo[1:]:
        robot.send_coords(coord_escritura(*punto, PLANO_Z), SPEED_DRAW)
        robot.wait_until_stopped()

    robot.send_coords(coord_escritura(*trazo[-1], Z_LEVANTE), SPEED_DRAW)
    robot.wait_until_stopped()

robot.set_color(0, 255, 0)
print("\n  K completada.")

robot.go_home()
robot.wait_until_stopped()
robot.gripper_open()
robot.set_color(0, 0, 0)

# ---------------------------------------------------------------------------
# Visualización de la trayectoria teórica
# ---------------------------------------------------------------------------

SALIDA = Path(__file__).parent / "escritura_K.png"

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5, 8))

    colores_trazo = ["royalblue", "tomato", "seagreen"]
    nombres_trazo = ["Palo vertical", "Diagonal superior", "Diagonal inferior"]

    for trazo, color, nombre in zip(TRAZOS, colores_trazo, nombres_trazo):
        xs = [ORIGEN_X + dx for dx, dy in trazo]
        ys = [ORIGEN_Y + dy for dx, dy in trazo]
        ax.plot(xs, ys, "-o", color=color, linewidth=2, markersize=6, label=nombre)
        if len(trazo) >= 2:
            ax.annotate("", xy=(xs[1], ys[1]), xytext=(xs[0], ys[0]),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5))

    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_title(f"Trayectoria teórica — K  (Z={PLANO_Z} mm)")
    ax.legend()
    ax.set_aspect("equal")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(SALIDA, dpi=150)
    print(f"  Gráfico guardado: {SALIDA.name}")

except ImportError:
    print("  pip install matplotlib  para visualización")
