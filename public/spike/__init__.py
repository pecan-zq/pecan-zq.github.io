import math, time
from ev3dev2.motor import MoveSteering, MoveTank
from ev3dev2.motor import LargeMotor
from ev3dev2.sensor.lego import GyroSensor, UltrasonicSensor
from ev3dev2.sensor.lego import ColorSensor as Ev3ColorSensor

# Map Spike Prime ports to Ev3 ports.
def map_port(port):
    if port == 'A':
        return 'outA'
    elif port == 'B':
        return 'outB'
    elif port == 'E':
        return 'in1'
    elif port == 'F':
        return 'in2'
    elif port == 'G':
        return 'in3'
    else:
        return None

def clip(n):
    n = n // 2
    if n < -100:
        return -100
    elif n > 100:
        return 100
    else:
        return n

class MotionSensor:
    def __init__(self):
        self.gyro_sensor = GyroSensor('in4')
    def reset_yaw_angle(self):
        self.gyro_sensor.reset()
    def get_yaw_angle(self):
        return self.gyro_sensor.angle

class PrimeHub:
    def __init__(self):
        self.gyro_sensor = MotionSensor()
    @property
    def motion_sensor(self):
        return self.gyro_sensor

class Motor:
    def __init__(self, port):
        port = map_port(port)
        self.motor = LargeMotor(port) if port is not None else None
        self.default_speed = 100
    def get_default_speed(self):
        return self.default_speed
    def set_default_speed(self, speed):
        self.default_speed = speed
    def set_degrees_counted(self, degrees):
        if self.motor is not None:
            self.motor.position = degrees
    def get_degrees_counted(self):
        if self.motor is not None:
            return self.motor.position
        else:
            return None
    def run_for_degrees(self, degrees, speed=None):
        speed = speed if speed is not None else self.default_speed
        if self.motor is not None:
            self.motor.on_for_degrees(speed=clip(speed), degrees=degrees)
        else:
            time.sleep(1)

class MotorPair:
    def __init__(self, left, right):
        left = map_port(left)
        right = map_port(right)
        self.tank_drive = MoveTank(left, right)
        self.steering_drive = MoveSteering(left, right)
        self.default_speed = 100
        self.wheel_width = 5.6
        self.brake = True
    def get_default_speed(self):
        return self.default_speed
    def set_default_speed(self, speed):
        self.default_speed = speed
    def set_motor_rotation(self, amount, unit='cm'):
        amount = (2.54 * amount) if unit == "in" else amount
        self.wheel_width = amount / math.pi
    def set_stop_action(self, action):
        self.brake = action == 'brake'
    def start_at_power(self, power=None, steering=0):
        power = power if power is not None else self.default_speed
        self.steering_drive.on(steering=clip(steering), speed=clip(power))
    def start(self, steering=0, speed=None):
        self.start_at_power(power=speed, steering=steering)
    def start_tank(self, left_speed, right_speed):
        self.tank_drive.on(
            left_speed=clip(left_speed),
            right_speed=clip(right_speed))
    def start_tank_at_power(self, left_power, right_power):
        self.start_tank(left_speed=left_power, right_speed=right_power)
    def move(self, amount, unit='cm', steering=0, speed=None):
        amount = (2.54 * amount) if unit == "in" else amount
        speed = speed if speed is not None else self.default_speed
        self.steering_drive.on_for_degrees(
            steering=clip(steering), speed=clip(speed),
            degrees=(amount * 360 / (math.pi * self.wheel_width)))
    def move_tank(self, amount, unit='cm', left_speed=None, right_speed=None):
        amount = (2.54 * amount) if unit == "in" else amount
        left_speed = left_speed if left_speed is not None else self.default_speed
        right_speed = right_speed if right_speed is not None else self.default_speed
        self.tank_drive.on_for_degrees(
            left_speed=clip(left_speed), right_speed=clip(right_speed),
            degrees=(amount * 360 / (math.pi * self.wheel_width)))
    def stop(self):
        self.steering_drive.off(brake=self.brake)

class ColorSensor:
    def __init__(self, port):
        self.color_sensor = Ev3ColorSensor(map_port(port))
    def get_reflected_light(self):
        return self.color_sensor.reflected_light_intensity
    def get_color(self):
        return self.color_sensor.color_name
    def get_ambient_light(self):
        return self.color_sensor.ambient_light_intensity

class DistanceSensor:
    def __init__(self, port):
        self.ultrasonic_sensor = UltrasonicSensor(map_port(port))
    def get_distance_cm(self, short_range=False):
        return self.ultrasonic_sensor.distance_centimeters
    def get_distance_inches(self, short_range=False):
        return self.ultrasonic_sensor.distance_inches
