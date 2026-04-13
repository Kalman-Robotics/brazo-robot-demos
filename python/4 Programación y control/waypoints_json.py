"""
Demo: Ejecución de waypoints desde archivo JSON

Lee una lista de poses desde un archivo .json y las recorre en orden.
Soporta poses angulares (flag=0) y cartesianas (flag=1).

Formato:
    [{"flag": 0, "pose": [J1..J6], "speed": 10, "label": "home"}, ...]

Uso:
    python waypoints_json.py
    python waypoints_json.py mi_secuencia.json
"""

import json
import sys
from pathlib import Path
from time import sleep
from kalman_robot_arm import KalmanRobotArm

ARCHIVO_DEFAULT = "waypoints_ejemplo.json"
PAUSA_ENTRE_POSES = 0.5

archivo = sys.argv[1] if len(sys.argv) > 1 else ARCHIVO_DEFAULT
ruta = Path(__file__).parent / archivo

if not ruta.exists():
    print(f"  Error: no se encontró '{archivo}'")
    sys.exit(1)

with open(ruta) as f:
    waypoints = json.load(f)

robot = KalmanRobotArm()
robot.set_color(0, 0, 255)

print(f"\n  Archivo: {archivo}  |  {len(waypoints)} waypoints\n")

for i, wp in enumerate(waypoints):
    flag  = wp.get("flag", 0)
    pose  = wp.get("pose")
    speed = wp.get("speed", 10)
    label = wp.get("label", f"wp{i+1}")
    tipo  = "ángulos" if flag == 0 else "coords"

    if pose is None:
        print(f"  [{i+1:02d}] {label} — pose no definida, omitiendo")
        continue

    robot.set_color(255, 165, 0)
    print(f"  [{i+1:02d}] {label}  ({tipo}, speed={speed})")

    if flag == 0:
        robot.send_angles(pose, speed)
    else:
        robot.send_coords(pose, speed)

    llego = robot.wait_until_stopped(timeout=30)
    if not llego:
        print(f"       Timeout esperando llegada a {label}")

    robot.set_color(0, 255, 0)
    sleep(PAUSA_ENTRE_POSES)

print("\n  Secuencia completada.")
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
