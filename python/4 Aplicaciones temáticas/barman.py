"""
Demo: Robot barman

Secuencia coreográfica que simula agarrar un "vaso", trasladarlo
y "servirlo" inclinando el extremo. Puramente visual.

Uso:
    python barman.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep

# Reposo — posición home
POSE_REPOSO        = [0, 0, 0, 0, 0, 0]

# Agarre del vaso — tomadas de pick_place_basico (posición A)
POSE_VASO_APPROACH = [-0.6, -26.5, -69.1, 13.3,  0.0, 0]
POSE_VASO_PICK     = [-0.6, -42.7, -83.0, 42.2,  0.0, 0]

INCLINACION = 10.0
POSE_SERVIR        = [83.1, -59.4, -38.7, 13.9 + INCLINACION, 0.0, 0]

# Devolver — mismo punto de pick (deja el vaso donde lo tomó)
POSE_DEVOLVER      = [-0.6, -42.7, -83.0, 42.2,  0.0, 0]

SPEED          = 20
SPEED_PICK     = 10
ESPERA_GRIPPER = 1.0
DURACION_SERVIR = 6.0

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
