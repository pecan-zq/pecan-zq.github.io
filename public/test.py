# A demo program written for Spike Prime to accomplish FLL Cargo Connect missions.
# Click Run button to run the program in simulator mode.
# To change settings like robot start position etc, go to menu MCU -> Settings.

# Import modules
from spike import ColorSensor, DistanceSensor, MotorPair, PrimeHub
from spike.control import wait_for_seconds, wait_until
from spike.operator import equal_to, less_than_or_equal_to

# Parameters
BLACK = 36
WHITE = 97
THRESHOLD = (BLACK + WHITE) / 2

motion_sensor = PrimeHub().motion_sensor
motion_sensor.reset_yaw_angle()
motor_pair = MotorPair('A', 'B')
color_sensor = ColorSensor('E')
distance_sensor = DistanceSensor('F')

print(color_sensor.get_color())
print(color_sensor.get_reflected_light())
print(color_sensor.get_ambient_light())