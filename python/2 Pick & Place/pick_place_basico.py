"""
Demo: Pick & Place básico

Recoge un objeto de la posición A y lo deposita en B.
Verifica get_gripper_status()==2 en bucle antes de continuar.
Si no hay agarre, reintenta hasta MAX_REINTENTOS.

Uso:
    python pick_place_basico.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep

POSE_HOME       = [0, 0, 0, 0, 0, 0]

POSE_A_APPROACH = [-0.6, -26.5, -69.1, 13.3, 0, 0]
POSE_A_PICK     = [-0.6, -42.7, -83.0, 42.2, 0, 0]

POSE_B_APPROACH = [43.1, -59.4, -38.7, 13.9, 0, 0]
POSE_B_PLACE    = [43.1, -70.3, -26.1, 10.3, 0, 0]

SPEED          = 20
SPEED_PICK     = 10
MAX_REINTENTOS = 3
ESPERA_GRIPPER = 1.2

PENDIENTES = {
    "POSE_A_APPROACH": POSE_A_APPROACH,
    "POSE_A_PICK":     POSE_A_PICK,
    "POSE_B_APPROACH": POSE_B_APPROACH,
    "POSE_B_PLACE":    POSE_B_PLACE,
}
faltantes = [k for k, v in PENDIENTES.items() if v is None]
if faltantes:
    print(f"\n  ⚠  Poses pendientes: {faltantes}")
    exit(0)

robot = KalmanRobotArm()
robot.gripper_open()
sleep(ESPERA_GRIPPER)

print("\n  Pick & Place — iniciando\n")

for intento in range(1, MAX_REINTENTOS + 1):
    print(f"  Intento {intento}/{MAX_REINTENTOS}")

    robot.set_color(0, 0, 255)
    robot.send_angles(POSE_HOME, SPEED)
    robot.wait_until_stopped()

    robot.set_color(255, 165, 0)
    robot.send_angles(POSE_A_APPROACH, SPEED)
    robot.wait_until_stopped()

    robot.send_angles(POSE_A_PICK, SPEED_PICK)
    robot.wait_until_stopped()

    robot.gripper_close()
    sleep(ESPERA_GRIPPER)

    status = robot.get_gripper_status()
    print(f"     gripper_status = {status}", end="")

    if status == 2:
        print("  → agarre OK")
        robot.set_color(0, 255, 0)
        break
    else:
        print("  → sin agarre, reintentando")
        robot.gripper_open()
        sleep(ESPERA_GRIPPER)
        robot.send_angles(POSE_A_APPROACH, SPEED)
        robot.wait_until_stopped()
else:
    robot.set_color(255, 0, 0)
    print(f"\n  Sin agarre tras {MAX_REINTENTOS} intentos. Abortando.")
    robot.go_home()
    robot.wait_until_stopped()
    robot.set_color(0, 0, 0)
    exit(1)

robot.send_angles(POSE_A_APPROACH, SPEED)
robot.wait_until_stopped()

robot.set_color(255, 165, 0)
robot.send_angles(POSE_B_APPROACH, SPEED)
robot.wait_until_stopped()

robot.send_angles(POSE_B_PLACE, SPEED_PICK)
robot.wait_until_stopped()

robot.gripper_open()
sleep(ESPERA_GRIPPER)
robot.set_color(0, 255, 0)
print("  Objeto depositado en B.")

robot.send_angles(POSE_B_APPROACH, SPEED)
robot.wait_until_stopped()
robot.go_home()
robot.wait_until_stopped()

print("\n  Pick & Place completado.")
robot.set_color(0, 0, 0)
