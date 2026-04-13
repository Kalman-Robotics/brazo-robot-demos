"""
Demo: Distribución 1-a-N (línea de producción)

Recoge desde un punto fijo y distribuye en secuencia a N posiciones
de depósito. Cicla por los destinos en orden.

Las poses de origen se toman de pick_place_basico. Los destinos comparten
la configuración J2..J6 de la posición B y solo varían en J1 (base),
separando las zonas de depósito en abanico sin alterar el origen.

Uso:
    python distribucion_1_a_N.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep

# Origen — tomado de pick_place_basico
POSE_ORIGEN_APPROACH = [-0.6, -26.5, -69.1, 13.3, 0, 0]
POSE_ORIGEN          = [-0.6, -42.7, -83.0, 42.2, 0, 0]

# Destinos — J2..J6 de la posición B, J1 varía por destino
_APPROACH_J2_J6 = [-59.4, -38.7, 13.9, 0, 0]
_PLACE_J2_J6    = [-70.3, -26.1, 10.3, 0, 0]

DESTINOS_J1 = [25.0, 43.1, 61.0]   # ángulo de base para cada zona de depósito

POSES_DESTINO_APPROACH = [[j1] + _APPROACH_J2_J6 for j1 in DESTINOS_J1]
POSES_DESTINO          = [[j1] + _PLACE_J2_J6    for j1 in DESTINOS_J1]

N_CICLOS       = 1
SPEED          = 20
SPEED_PICK     = 10
ESPERA_GRIPPER = 1.2

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
        print(f"  Pieza {pieza:02d}/{total_piezas}  →  destino {idx + 1}  (J1={DESTINOS_J1[idx]}°)")

        robot.set_color(255, 165, 0)
        robot.send_angles(POSE_ORIGEN_APPROACH, SPEED)
        robot.wait_until_stopped()
        robot.send_angles(POSE_ORIGEN, SPEED_PICK)
        robot.wait_until_stopped()

        robot.gripper_close()
        sleep(ESPERA_GRIPPER)

        robot.send_angles(POSE_ORIGEN_APPROACH, SPEED)
        robot.wait_until_stopped()
        robot.send_angles(POSES_DESTINO_APPROACH[idx], SPEED)
        robot.wait_until_stopped()

        robot.send_angles(pose_destino, SPEED_PICK)
        robot.wait_until_stopped()
        robot.gripper_open()
        sleep(ESPERA_GRIPPER)
        robot.set_color(0, 255, 0)

        robot.send_angles(POSES_DESTINO_APPROACH[idx], SPEED)
        robot.wait_until_stopped()

print(f"\n  Distribución completada — {total_piezas} piezas distribuidas.")
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
