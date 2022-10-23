# A demo program written for Spike Prime to accomplish FLL Cargo Connect missions.
# Click Run button to run the program in simulator mode.
# To change settings like robot start position etc, go to menu MCU -> Settings.

# Import modules
from spike import ColorSensor, DistanceSensor, MotorPair, PrimeHub
from spike.control import wait_for_seconds, wait_until, Timer
from spike.operator import less_than, less_than_or_equal_to, greater_than, greater_than_or_equal_to, equal_to

motion_sensor = PrimeHub().motion_sensor
motion_sensor.reset_yaw_angle()
motor_pair = MotorPair('A', 'B')
left_color_sensor = ColorSensor('E')
right_color_sensor = ColorSensor('F')
distance_sensor = DistanceSensor('G')
timer = Timer()


def turn(angle) :
    max_power = 100
    min_power = 10
    net_power = max_power - min_power
    if motion_sensor.get_yaw_angle() < angle :
        while motion_sensor.get_yaw_angle() < angle :
            turn_power = min_power + abs(motion_sensor.get_yaw_angle() - angle) / 180 * net_power
            motor_pair.start_tank_at_power(turn_power, -turn_power)
        motor_pair.stop()
    else:
        while motion_sensor.get_yaw_angle() >= angle :
            turn_power = min_power + abs(motion_sensor.get_yaw_angle() - angle) / 180 * net_power
            motor_pair.start_tank_at_power(-turn_power, turn_power)
        motor_pair.stop()


def follow_line(speed=50):
    BLACK = 36
    WHITE = 97
    THRESHOLD = (BLACK + WHITE) / 2
    PROPORTIONAL_GAIN = 3
    BLACK_OUT_SECOND = 1
    timer.reset()

    while True:
        deviation = left_color_sensor.get_reflected_light() - THRESHOLD
        turn_rate = int(PROPORTIONAL_GAIN * deviation)
        motor_pair.start_at_power(steering=turn_rate, power=speed)
        if timer.now() > BLACK_OUT_SECOND and right_color_sensor.get_reflected_light() < 50 :
            motor_pair.stop()
            break


turn(180)

#motor_pair.move(20, speed = 40)
#turn(30)
#motor_pair.move(5, speed = 40)
#follow_line(40)
#turn(-90)
#motor_pair.move(-5, speed = 40)
#turn(70)
#motor_pair.move(6, speed = 40)
#follow_line(40)
#turn(90)
#motor_pair.move(2, speed = 40)
#turn(0)
#motor_pair.move(-3, speed = 40)
#turn(180)
#follow_line(40)

#vector_list = [(10, 0), (20, 30), (40, -30), (70, 120)]
#for vec in vector_list :
#    move_vector(vec)

