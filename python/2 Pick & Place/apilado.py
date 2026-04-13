"""
Demo: Apilado de objetos

Recoge un objeto de posición fija e incrementa el Z de depósito
en cada ciclo para simular apilado. El número de capas es configurable.

Poses a calibrar con el CEO:
  POSE_PICK_APPROACH   — sobre la posición de recogida
  POSE_PICK            — posición de recogida (contacto)
  POSE_STACK_APPROACH  — sobre la zona de apilado
  POSE_STACK_BASE      — primera posición de depósito [x, y, z, rx, ry, rz]

Uso:
    python apilado.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep

POSE_PICK_APPROACH   = None   # TODO: [J1..J6]
POSE_PICK            = None   # TODO: [J1..J6]
POSE_STACK_APPROACH  = None   # TODO: [J1..J6]
POSE_STACK_BASE      = None   # TODO: [x, y, z, rx, ry, rz]

N_CAPAS         = 4
ALTURA_OBJETO   = 35.0
SPEED           = 10
SPEED_PICK      = 6
ESPERA_GRIPPER  = 1.2

PENDIENTES = {
    "POSE_PICK_APPROACH":  POSE_PICK_APPROACH,
    "POSE_PICK":           POSE_PICK,
    "POSE_STACK_APPROACH": POSE_STACK_APPROACH,
    "POSE_STACK_BASE":     POSE_STACK_BASE,
}
faltantes = [k for k, v in PENDIENTES.items() if v is None]
if faltantes:
    print(f"\n  ⚠  Poses pendientes: {faltantes}")
    exit(0)

robot = KalmanRobotArm()
robot.gripper_open()
sleep(ESPERA_GRIPPER)

print(f"\n  Apilado — {N_CAPAS} capas × {ALTURA_OBJETO}mm/capa\n")

for capa in range(N_CAPAS):
    z_deposito = POSE_STACK_BASE[2] + capa * ALTURA_OBJETO
    pose_deposito = list(POSE_STACK_BASE)
    pose_deposito[2] = z_deposito

    print(f"  Capa {capa + 1}/{N_CAPAS}  (Z depósito = {z_deposito:.1f}mm)")

    robot.set_color(255, 165, 0)
    robot.send_angles(POSE_PICK_APPROACH, SPEED)
    robot.wait_until_stopped()
    robot.send_angles(POSE_PICK, SPEED_PICK)
    robot.wait_until_stopped()

    robot.gripper_close()
    sleep(ESPERA_GRIPPER)

    if robot.get_gripper_status() != 2:
        robot.set_color(255, 0, 0)
        print(f"  Sin agarre en capa {capa + 1}. Abortando.")
        robot.gripper_open()
        robot.go_home()
        robot.wait_until_stopped()
        exit(1)

    robot.set_color(0, 255, 0)
    robot.send_angles(POSE_PICK_APPROACH, SPEED)
    robot.wait_until_stopped()

    robot.set_color(255, 165, 0)
    robot.send_angles(POSE_STACK_APPROACH, SPEED)
    robot.wait_until_stopped()
    robot.send_coords(pose_deposito, SPEED_PICK)
    robot.wait_until_stopped()

    robot.gripper_open()
    sleep(ESPERA_GRIPPER)
    robot.set_color(0, 255, 0)

    robot.send_angles(POSE_STACK_APPROACH, SPEED)
    robot.wait_until_stopped()

print(f"\n  Apilado completado — {N_CAPAS} capas.")
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
