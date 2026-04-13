import math
from time import sleep
from kalman_robot_arm import KalmanRobotArm

robot = KalmanRobotArm()
robot.go_home()
robot.gripper_open()

print(robot.get_angles())
print(robot.get_coords())
