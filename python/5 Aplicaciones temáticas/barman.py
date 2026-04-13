"""
Demo: Robot barman

Secuencia coreográfica que simula agarrar un "vaso", trasladarlo
y "servirlo" inclinando el extremo. Puramente visual.

Poses a calibrar con el CEO:
  POSE_REPOSO, POSE_VASO_APPROACH, POSE_VASO_PICK, POSE_SERVIR, POSE_DEVOLVER

Uso:
    python barman.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep

POSE_REPOSO        = None   # TODO: [J1..J6]
POSE_VASO_APPROACH = None   # TODO: [J1..J6]
POSE_VASO_PICK     = None   # TODO: [J1..J6]
POSE_SERVIR        = None   # TODO: [J1..J6]
POSE_DEVOLVER      = None   # TODO: [J1..J6]

SPEED          = 10
SPEED_PICK     = 6
ESPERA_GRIPPER = 1.0
DURACION_SERVIR = 1.5

PENDIENTES = {
    "POSE_REPOSO":        POSE_REPOSO,
    "POSE_VASO_APPROACH": POSE_VASO_APPROACH,
    "POSE_VASO_PICK":     POSE_VASO_PICK,
    "POSE_SERVIR":        POSE_SERVIR,
    "POSE_DEVOLVER":      POSE_DEVOLVER,
}
faltantes = [k for k, v in PENDIENTES.items() if v is None]
if faltantes:
    print(f"\n  ⚠  Poses pendientes: {faltantes}")
    exit(0)

robot = KalmanRobotArm()
robot.gripper_open()
sleep(ESPERA_GRIPPER)

print("\n  Robot Barman — iniciando\n")

robot.set_color(0, 255, 0)
robot.send_angles(POSE_REPOSO, SPEED)
robot.wait_until_stopped()
sleep(0.5)

print("  → Aproximando al vaso")
robot.set_color(255, 165, 0)
robot.send_angles(POSE_VASO_APPROACH, SPEED)
robot.wait_until_stopped()

robot.send_angles(POSE_VASO_PICK, SPEED_PICK)
robot.wait_until_stopped()
robot.gripper_close()
sleep(ESPERA_GRIPPER)
print(f"     gripper_status = {robot.get_gripper_status()}")

robot.send_angles(POSE_VASO_APPROACH, SPEED)
robot.wait_until_stopped()

print("  → Sirviendo")
robot.set_color(0, 0, 255)
robot.send_angles(POSE_SERVIR, SPEED)
robot.wait_until_stopped()
sleep(DURACION_SERVIR)

print("  → Devolviendo vaso")
robot.set_color(255, 165, 0)
robot.send_angles(POSE_VASO_APPROACH, SPEED)
robot.wait_until_stopped()
robot.send_angles(POSE_DEVOLVER, SPEED_PICK)
robot.wait_until_stopped()
robot.gripper_open()
sleep(ESPERA_GRIPPER)

robot.send_angles(POSE_VASO_APPROACH, SPEED)
robot.wait_until_stopped()
robot.send_angles(POSE_REPOSO, SPEED)
robot.wait_until_stopped()

robot.set_color(0, 255, 0)
print("\n  Servido. ¡Salud!")
sleep(1)
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
