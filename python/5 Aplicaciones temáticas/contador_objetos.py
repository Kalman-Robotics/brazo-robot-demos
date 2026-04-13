"""
Demo: Contador de objetos

El robot recoge objetos de una bandeja uno por uno.
Cada 10s muestra en consola el conteo acumulado de agarres exitosos.

Uso:
    python contador_objetos.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep, time

POSE_BANDEJA_APPROACH = [-0.6, -26.5, -69.1, 13.3, 0, 0]
POSE_BANDEJA          = [-0.6, -42.7, -83.0, 42.2, 0, 0]

POSE_DESCARGA_APPROACH = [43.1, -59.4, -38.7, 13.9, 0, 0]
POSES_DESCARGA = [
    [43.1, -70.3, -26.1, 10.3, 0, 0],
    [43.1, -70.3, -26.1, 10.3, 0, 0],
    [43.1, -70.3, -26.1, 10.3, 0, 0],
]

N_MAX_OBJETOS        = 10
MAX_INTENTOS_VACIADA = float('inf')
INTERVALO_DISPLAY    = 10.0
SPEED                = 10
SPEED_PICK           = 6
ESPERA_GRIPPER       = 1.2

def mostrar_display(total, ultimo_estado):
    print(f"\n  ┌─────────────────────────────┐")
    print(f"  │  Objetos procesados: {total:<6d}  │")
    print(f"  │  Último agarre: {ultimo_estado:<12s} │")
    print(f"  └─────────────────────────────┘\n")

robot = KalmanRobotArm()
robot.gripper_open()
sleep(ESPERA_GRIPPER)

print(f"\n  Contador de objetos — máx {N_MAX_OBJETOS} piezas\n")

total_ok      = 0
intentos_vacios = 0
ultimo_estado = "---"
t_ultimo_display = time()
destino_idx = 0

for ciclo in range(N_MAX_OBJETOS):
    if time() - t_ultimo_display >= INTERVALO_DISPLAY:
        mostrar_display(total_ok, ultimo_estado)
        t_ultimo_display = time()

    print(f"  Intento {ciclo + 1}/{N_MAX_OBJETOS}")

    robot.set_color(255, 165, 0)
    robot.send_angles(POSE_BANDEJA_APPROACH, SPEED)
    robot.wait_until_stopped()
    robot.send_angles(POSE_BANDEJA, SPEED_PICK)
    robot.wait_until_stopped()

    robot.gripper_close()
    sleep(ESPERA_GRIPPER)
    status = robot.get_gripper_status()

    if status == 2:
        total_ok += 1
        intentos_vacios = 0
        ultimo_estado = "OK"
        robot.set_color(0, 255, 0)
        print(f"     Agarre OK  |  Total: {total_ok}")

        robot.send_angles(POSE_BANDEJA_APPROACH, SPEED)
        robot.wait_until_stopped()
        robot.send_angles(POSE_DESCARGA_APPROACH, SPEED)
        robot.wait_until_stopped()

        pose_dest = POSES_DESCARGA[destino_idx % len(POSES_DESCARGA)]
        robot.send_angles(pose_dest, SPEED_PICK)
        robot.wait_until_stopped()
        robot.gripper_open()
        sleep(ESPERA_GRIPPER)
        destino_idx += 1

        robot.send_angles(POSE_DESCARGA_APPROACH, SPEED)
        robot.wait_until_stopped()

    else:
        ultimo_estado = "FALLO"
        intentos_vacios += 1
        robot.set_color(255, 0, 0)
        print(f"     Sin agarre  |  intentos vacíos: {intentos_vacios}")

        robot.gripper_open()
        sleep(ESPERA_GRIPPER)
        robot.send_angles(POSE_BANDEJA_APPROACH, SPEED)
        robot.wait_until_stopped()

        if intentos_vacios >= MAX_INTENTOS_VACIADA:
            print(f"\n  Bandeja vacía detectada.")
            break

mostrar_display(total_ok, ultimo_estado)
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
