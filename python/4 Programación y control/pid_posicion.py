"""
Demo: Control PID de posición en Python

Bucle de control proporcional sobre J1.
Lee get_angle(1) en cada iteración, calcula el error respecto al setpoint
y envía una corrección proporcional hasta converger o agotar el timeout.

No requiere calibración de poses.

Uso:
    python pid_posicion.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep, time

SETPOINT   = 45.0
KP         = 0.4
TOLERANCIA = 0.50
TIMEOUT    = 15.0
DT         = 0.1
SPEED_BASE = 20

robot = KalmanRobotArm()

print("\n  Control proporcional J1")
print(f"  Setpoint: {SETPOINT}°  |  Kp: {KP}  |  Tolerancia: ±{TOLERANCIA}°")
print(f"  {'Tiempo':>7}  {'Setpoint':>9}  {'Posición':>9}  {'Error':>7}  {'Cmd':>6}")
print("  " + "─" * 46)

robot.set_color(0, 0, 255)

t_inicio = time()
convergido = False

while (time() - t_inicio) < TIMEOUT:
    pos_actual = robot.get_angle(1)
    if pos_actual is None or pos_actual == -1:
        sleep(DT)
        continue

    error = SETPOINT - pos_actual
    t_rel = time() - t_inicio

    cmd = pos_actual + KP * error
    cmd = max(-120.0, min(120.0, cmd))

    print(f"  {t_rel:>6.2f}s  {SETPOINT:>8.2f}°  {pos_actual:>8.2f}°  "
          f"{error:>+6.2f}°  {cmd:>5.1f}°")

    if abs(error) <= TOLERANCIA:
        convergido = True
        break

    robot.send_angle(1, cmd, SPEED_BASE)
    sleep(DT)

robot.wait_until_stopped(timeout=5)

if convergido:
    robot.set_color(0, 255, 0)
    print(f"\n  Convergido en {time() - t_inicio:.2f}s")
else:
    robot.set_color(255, 0, 0)
    print(f"\n  Timeout — posición final: {robot.get_angle(1):.2f}°")

print()
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
