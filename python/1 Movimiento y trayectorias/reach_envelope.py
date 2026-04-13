"""
Demo: Reach Envelope — nube de puntos del workspace real

Recorre combinaciones de ángulos articulares dentro de un rango seguro
y registra la posición cartesiana real con get_coords() en cada punto.
Genera un archivo CSV y una visualización 3D con matplotlib.

Uso:
    python reach_envelope.py
"""

import csv
from pathlib import Path
from time import sleep
from kalman_robot_arm import KalmanRobotArm

RANGO_J1 = range(-90, 91, 30)
RANGO_J2 = range(-70, 71, 30)

J3_FIJO = 0
J4_FIJO = 0
J5_FIJO = 0
J6_FIJO = 0

SPEED        = 15
ESPERA_POST  = 0.3
CSV_SALIDA   = Path(__file__).parent / "workspace_points.csv"

robot = KalmanRobotArm()
robot.set_color(0, 0, 255)

total_poses = len(list(RANGO_J1)) * len(list(RANGO_J2))
print(f"\n  Reach Envelope — {total_poses} poses a recorrer")

puntos = []

for j1 in RANGO_J1:
    for j2 in RANGO_J2:
        angles = [j1, j2, J3_FIJO, J4_FIJO, J5_FIJO, J6_FIJO]
        robot.set_color(255, 165, 0)
        robot.send_angles(angles, SPEED)
        llego = robot.wait_until_stopped(timeout=20)

        if not llego:
            print(f"  [SKIP] J1={j1:4d}° J2={j2:4d}° — timeout")
            continue

        sleep(ESPERA_POST)
        coords = robot.get_coords()

        if not isinstance(coords, list) or len(coords) != 6:
            print(f"  [SKIP] J1={j1:4d}° J2={j2:4d}° — coords inválidas")
            continue

        x, y, z = coords[0], coords[1], coords[2]
        puntos.append((j1, j2, *coords))
        robot.set_color(0, 255, 0)
        print(f"  J1={j1:4d}° J2={j2:4d}°  →  x={x:7.1f} y={y:7.1f} z={z:7.1f}")

with open(CSV_SALIDA, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["j1", "j2", "x", "y", "z", "rx", "ry", "rz"])
    writer.writerows(puntos)

print(f"\n  {len(puntos)} puntos registrados → {CSV_SALIDA.name}")

robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

    xs = [p[2] for p in puntos]
    ys = [p[3] for p in puntos]
    zs = [p[4] for p in puntos]

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")
    sc = ax.scatter(xs, ys, zs, c=zs, cmap="viridis", s=20, alpha=0.7)
    plt.colorbar(sc, ax=ax, label="Z (mm)")
    ax.set_xlabel("X (mm)")
    ax.set_ylabel("Y (mm)")
    ax.set_zlabel("Z (mm)")
    ax.set_title("Workspace — myCobot Pro 450")
    plt.tight_layout()
    plt.savefig(Path(__file__).parent / "workspace_3d.png", dpi=150)
    plt.show()
    print("  Gráfico guardado: workspace_3d.png")

except ImportError:
    print("  matplotlib no instalado — omitiendo visualización")
    print("  pip install matplotlib")
