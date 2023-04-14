import time
import math
from servo import Servo, servo2040

# Define the segment lengths of the robot arm
L1 = 5.0  # length of the base segment
L2 = 7.0  # length of the shoulder segment
L3 = 5.0  # length of the elbow segment
L4 = 3.0  # length of the wrist segment

# Define the minimum and maximum angles for each joint
MIN_ANGLE_BASE = -90
MAX_ANGLE_BASE = 90
MIN_ANGLE_SHOULDER = -90
MAX_ANGLE_SHOULDER = 90
MIN_ANGLE_ELBOW = -90
MAX_ANGLE_ELBOW = 90
MIN_ANGLE_WRIST = -90
MAX_ANGLE_WRIST = 90

# Create a list of servos for each joint of the robot arm
pwm_base = servo2040.SERVO_1
pwm_shoulder = servo2040.SERVO_2
pwm_elbow = servo2040.SERVO_3
pwm_wrist = servo2040.SERVO_4
servos = [Servo(i) for i in [pwm_base, pwm_shoulder, pwm_elbow, pwm_wrist]]

# Enable all servos (this puts them at the middle)
for s in servos:
    s.enable()
time.sleep(2)

# Define the target coordinates for the end effector
x = 6.0
y = 3.0
z = 8.0

# Compute the joint angles using inverse kinematics
# Calculate the angle of the base joint
base_angle = math.degrees(math.atan2(y, x))

# Calculate the distance from the base joint to the end effector
d = math.sqrt(x**2 + y**2) - L4

# Calculate the angle of the shoulder joint
a = math.sqrt(d**2 + z**2)
b = math.sqrt(L2**2 + L3**2)
c = math.sqrt(d**2 + (z - L1)**2)
shoulder_angle = math.degrees(math.acos((a**2 + b**2 - c**2) / (2 * a * b)) - math.atan2(z - L1, d))

# Calculate the angle of the elbow joint
elbow_angle = math.degrees(math.acos((b**2 + c**2 - a**2) / (2 * b * c))) - 90

# Calculate the angle of the wrist joint
wrist_angle = math.degrees(math.atan2(z - L1 - a * math.sin(math.radians(shoulder_angle)), d + a * math.cos(math.radians(shoulder_angle)))) - shoulder_angle - elbow_angle

# Clip the joint angles to the minimum and maximum values
base_angle = min(max(base_angle, MIN_ANGLE_BASE), MAX_ANGLE_BASE)
shoulder_angle = min(max(shoulder_angle, MIN_ANGLE_SHOULDER), MAX_ANGLE_SHOULDER)
elbow_angle = min(max(elbow_angle, MIN_ANGLE_ELBOW), MAX_ANGLE_ELBOW)
wrist_angle = min(max(wrist_angle, MIN_ANGLE_WRIST), MAX_ANGLE_WRIST)

# Convert the joint angles to PWM duty cycles
base_duty = int((base_angle / 180) * 1000) + 500
shoulder_duty = int((shoulder_angle / 180) * 1000) + 500
elbow_duty = int((elbow_angle / 180) * 1000) + 500
wrist_duty = int((wrist_angle / 180) * 1000) + 500

# Set the servo positions to the computed duty cycles
servos[0].duty(base_duty)
servos[1].duty(shoulder_duty)
servos[2].duty(elbow_duty)
servos[3].duty(wrist_duty)

# Wait for the servos to move
time.sleep(1)

# Disable the servos
for s in servos:
    s.disable()

