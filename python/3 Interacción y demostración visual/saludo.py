"""
Demo: Saludo / wave

Secuencia de ángulos que simula un movimiento de saludo.
El CEO define los waypoints moviendo el robot a mano (modo libre)
y leyendo get_angles() en cada posición.

Uso:
    python saludo.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep

WAYPOINTS_SALUDO = [
    # {"label": "posicion_1", "angles": None,  "speed": 15},
    # {"label": "posicion_2", "angles": None,  "speed": 15},
]

REPETICIONES = 2

if not WAYPOINTS_SALUDO:
    print("\n  ⚠  WAYPOINTS_SALUDO está vacío.")
    print("  Completar con el CEO: mover el robot a mano, leer get_angles()")
    exit(0)

pendientes = [wp for wp in WAYPOINTS_SALUDO if wp.get("angles") is None]
if pendientes:
    labels = [wp.get("label", "?") for wp in pendientes]
    print(f"\n  ⚠  Poses pendientes: {labels}")
    exit(0)

robot = KalmanRobotArm()
robot.set_color(0, 255, 0)

print(f"\n  Saludo — {len(WAYPOINTS_SALUDO)} poses × {REPETICIONES} repeticiones\n")

for rep in range(REPETICIONES):
    print(f"  Repetición {rep + 1}/{REPETICIONES}")
    for wp in WAYPOINTS_SALUDO:
        robot.set_color(255, 165, 0)
        robot.send_angles(wp["angles"], wp.get("speed", 15))
        robot.wait_until_stopped(timeout=15)
        robot.set_color(0, 255, 0)
        sleep(0.1)
    sleep(0.3)

print("\n  Saludo completado.")
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
