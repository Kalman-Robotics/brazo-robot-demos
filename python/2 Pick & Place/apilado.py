"""
Demo: Apilado de 3 bloques con retorno

Secuencia:
  Fase 1 — Desapila A (capa 2 → 1 → 0) y apila en B (capa 0 → 1 → 2)
  Fase 2 — Home (espera)
  Fase 3 — Desapila B (capa 2 → 1 → 0) y reconstruye A (capa 0 → 1 → 2)

Uso:
    python apilado.py
"""

from kalman_robot_arm import KalmanRobotArm
from time import sleep

# ── Poses ─────────────────────────────────────────────────────────────────────
POSE_A_APPROACH  = [-0.6, -26.5, -69.1, 13.3, 0, 0]
POSE_A_PICK_L0   = [-0.6, -42.7, -83.0, 42.2, 0, 0]
POSE_A_PICK_L1   = [-0.59, -42.34, -72.97, 29.51, 0.0, 0.0]
POSE_A_PICK_L2   = [-0.59, -35.85, -75.73, 28.01, 0.0, 0.0]

POSE_B_APPROACH  = [42.84, -61.96, -11.95, -10.28, 0.0, 0.0]
POSE_B_PLACE_L0  = [42.81, -73.04, -23.9, 10.81, 0.0, 0.0]
POSE_B_PLACE_L1  = [42.53, -74.8, -9.93, -1.48, 0.0, 0.0]
POSE_B_PLACE_L2  = [42.88, -63.49, -22.27, -0.36, 0.0, 0.0]

SPEED           = 20
SPEED_PICK      = 10
ESPERA_GRIPPER  = 1.2
ESPERA_HOME     = 3.0

# ── Helpers ───────────────────────────────────────────────────────────────────
robot = KalmanRobotArm()

def pick(approach, pose):
    robot.set_color(255, 165, 0)
    robot.send_angles(approach, SPEED)
    robot.wait_until_stopped()
    robot.send_angles(pose, SPEED_PICK)
    robot.wait_until_stopped()
    robot.gripper_close()
    sleep(ESPERA_GRIPPER)
    robot.send_angles(approach, SPEED)
    robot.wait_until_stopped()

def place(approach, pose):
    robot.send_angles(approach, SPEED)
    robot.wait_until_stopped()
    robot.send_angles(pose, SPEED_PICK)
    robot.wait_until_stopped()
    robot.gripper_open()
    sleep(ESPERA_GRIPPER)
    robot.set_color(0, 255, 0)
    robot.send_angles(approach, SPEED)
    robot.wait_until_stopped()

# ── Secuencia de fases ────────────────────────────────────────────────────────
robot.gripper_open()
sleep(ESPERA_GRIPPER)

# Fase 1: A → B  (desapila A de arriba a abajo, apila B de abajo a arriba)
print("\n  Fase 1 — A → B\n")
PICKS_A  = [POSE_A_PICK_L2,  POSE_A_PICK_L1,  POSE_A_PICK_L0 ]
PLACES_B = [POSE_B_PLACE_L0, POSE_B_PLACE_L1, POSE_B_PLACE_L2]

for i, (a_pick, b_place) in enumerate(zip(PICKS_A, PLACES_B)):
    print(f"  Bloque {i+1}/3  (capa {2-i} → capa {i})")
    pick(POSE_A_APPROACH, a_pick)
    place(POSE_B_APPROACH, b_place)

# Fase 2: home
print("\n  Fase 2 — Home\n")
robot.set_color(0, 0, 255)
robot.go_home()
robot.wait_until_stopped()
sleep(ESPERA_HOME)

# Fase 3: B → A  (desapila B de arriba a abajo, reconstruye A de abajo a arriba)
print("\n  Fase 3 — B → A\n")
PICKS_B   = [POSE_B_PLACE_L2, POSE_B_PLACE_L1, POSE_B_PLACE_L0]
PLACES_A  = [POSE_A_PICK_L0,  POSE_A_PICK_L1,  POSE_A_PICK_L2 ]

for i, (b_pick, a_place) in enumerate(zip(PICKS_B, PLACES_A)):
    print(f"  Bloque {i+1}/3  (capa {2-i} → capa {i})")
    pick(POSE_B_APPROACH, b_pick)
    place(POSE_A_APPROACH, a_place)

print("\n  Apilado completado — bloques devueltos a A.")
robot.go_home()
robot.wait_until_stopped()
robot.set_color(0, 0, 0)
