"""
Demo: Distribución 1-a-N (línea de producción)

Recoge desde un punto fijo y distribuye en secuencia a N posiciones
de depósito. Cicla por los destinos en orden.

Uso:
    python distribucion_1_a_N.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep

POSE_ORIGEN_APPROACH = None   # TODO: [J1..J6]
POSE_ORIGEN          = None   # TODO: [J1..J6]
POSE_DESTINO_APPROACH_COMUN = None   # TODO: [J1..J6]

POSES_DESTINO = [
    None,   # TODO: destino 1
    None,   # TODO: destino 2
    None,   # TODO: destino 3
]

N_CICLOS       = 3
SPEED          = 10
SPEED_PICK     = 6
ESPERA_GRIPPER = 1.2

PENDIENTES = {
    "POSE_ORIGEN_APPROACH":        POSE_ORIGEN_APPROACH,
    "POSE_ORIGEN":                 POSE_ORIGEN,
    "POSE_DESTINO_APPROACH_COMUN": POSE_DESTINO_APPROACH_COMUN,
}
faltantes = [k for k, v in PENDIENTES.items() if v is None]
faltantes += [f"POSES_DESTINO[{i}]" for i, v in enumerate(POSES_DESTINO) if v is None]

if faltantes:
    print(f"\n  ⚠  Poses pendientes: {faltantes}")
    exit(0)

robot = KalmanRobotArm()
robot.gripper_open()
sleep(ESPERA_GRIPPER)

n_destinos = len(POSES_DESTINO)
total_piezas = N_CICLOS * n_destinos
print(f"\n  Distribución 1-a-{n_destinos}  |  {N_CICLOS} ciclo(s)  |  {total_piezas} piezas\n")

pieza = 0
for ciclo in range(N_CICLOS):
    for idx, pose_destino in enumerate(POSES_DESTINO):
        pieza += 1
        print(f"  Pieza {pieza:02d}/{total_piezas}  →  destino {idx + 1}")

        robot.set_color(255, 165, 0)
        robot.send_angles(POSE_ORIGEN_APPROACH, SPEED)
        robot.wait_until_stopped()
        robot.send_angles(POSE_ORIGEN, SPEED_PICK)
        robot.wait_until_stopped()

        robot.gripper_close()
        sleep(ESPERA_GRIPPER)

        if robot.get_gripper_status() != 2:
            robot.set_color(255, 0, 0)
            print(f"  Sin agarre en pieza {pieza}. Abortando.")
            robot.gripper_open()
            robot.go_home()
            robot.wait_until_stopped()
            exit(1)

        robot.send_angles(POSE_ORIGEN_APPROACH, SPEED)
        robot.wait_until_stopped()
        robot.send_angles(POSE_DESTINO_APPROACH_COMUN, SPEED)
        robot.wait_until_stopped()

        robot.send_angles(pose_destino, SPEED_PICK)
        robot.wait_until_stopped()
        robot.gripper_open()
        sleep(ESPERA_GRIPPER)
        robot.set_color(0, 255, 0)

        robot.send_angles(POSE_DESTINO_APPROACH_COMUN, SPEED)
        robot.wait_until_stopped()

print(f"\n  Distribución completada — {total_piezas} piezas distribuidas.")
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
