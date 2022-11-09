""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Motor pair mock
# -------------------------------------------------------
# Nadège LEMPERIERE,  @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# Local includes
from spike.mock import Mock
from spike.robot import Robot
from spike.motor import motor_stop_actions

# Constants
motorpair_units = [
    'cm',
    'inches',
    'rotations',
    'degrees',
    'seconds',
]

class MotorPair(Mock) :
    """ MotorPair mocking function """

    m_default_speed = 100
    m_stop_action   = 'brake'
    m_left_motor    = None
    m_right_motor   = None
    m_shared_robot  = None

    s_max_speed     = 100
    s_max_steering  = 100
    s_max_power     = 100

# -------------- SPIKE MOTORPAIR FUNCTIONS ---------------

    def __init__(self, left_motor, right_motor) :
        """ Contructor
        ---
        left_motor (str)    : The port on which the left motor is located
        right_motor (str)   : The port on which the right motor is located
        """

        super().__init__()
        self.m_shared_robot      = Robot()

        if  self.m_shared_robot.get_component(left_motor) is None or \
            self.m_shared_robot.get_component(left_motor) != 'Motor' :
            raise ValueError('Port ' + left_motor + ' does not host a motor')

        if  self.m_shared_robot.get_component(right_motor) is None or \
            self.m_shared_robot.get_component(right_motor) != 'Motor' :
            raise ValueError('Port ' + right_motor + ' does not host a motor')

        if  left_motor not in self.m_shared_robot.m_components :
            raise ValueError('Motor ' + left_motor + ' has not been initialized')
        if  right_motor not in self.m_shared_robot.m_components :
            raise ValueError('Motor ' + right_motor + ' has not been initialized')

        self.m_default_speed = 100
        self.m_stop_action   = 'brake'
        self.m_left_motor    = self.m_shared_robot.m_components[left_motor]
        self.m_right_motor   = self.m_shared_robot.m_components[right_motor]
        self.s_default_columns  = {
            'left degrees':'left degrees',
            'right degrees':'right degrees',
        }

    def move(self, amount, unit='cm', steering=0, speed=None) :
        """ Activate both motors to move from a given distance
        ---
        amount (float)  : Displacement value
        unit (str)      : Displacement unit
        steering (int)  : Direction and quantity to orient the base
        speed (int)     : Displacement speed
        """

        if speed is None : speed = self.m_default_speed

        if not isinstance(amount, (float, int)):
            raise TypeError('amount is not a number')
        if not isinstance(unit, str) :
            raise TypeError('unit is not a string')
        if not isinstance(steering, int) :
            raise TypeError('steering is not an integer')
        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        if unit not in motorpair_units :
            raise ValueError('unit is not one of the allowed values')

        speed = min(max(speed,- self.s_max_speed),self.s_max_speed)
        steering = min(max(steering,- self.s_max_steering),self.s_max_steering)

    def start(self, steering=0, speed=None) :
        """ Activate both motors
        ---
        steering (int)  : Direction and quantity to orient the base
        speed (int)     : Displacement speed
        """

        if speed is None : speed = self.m_default_speed

        if not isinstance(steering, int) :
            raise TypeError('steering is not an integer')
        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        speed = min(max(speed,- self.s_max_speed),self.s_max_speed)
        steering = min(max(steering,- self.s_max_steering),self.s_max_steering)

    def stop(self) :
        """ Stop base """

    def move_tank(self, amount, unit='cm', left_speed=None, right_speed=None) :
        """ Activate both motors to move from a given distance
        ---
        amount (float)    : Displacement value
        unit (str)        : Displacement unit
        left_speed (int)  : Left motor speed
        right_speed (int) : Right motor speed
        """

        if left_speed is None : left_speed = self.m_default_speed
        if right_speed is None : right_speed = self.m_default_speed

        if not isinstance(amount, (float, int)):
            raise TypeError('amount is not a number')
        if not isinstance(unit, str) :
            raise TypeError('unit is not a string')
        if not isinstance(left_speed, int) :
            raise TypeError('left_speed is not an integer')
        if not isinstance(right_speed, int) :
            raise TypeError('right_speed is not an integer')

        if unit not in motorpair_units :
            raise ValueError('unit is not one of the allowed values')

        left_speed = min(max(left_speed,- self.s_max_speed),self.s_max_speed)
        right_speed = min(max(right_speed,- self.s_max_speed),self.s_max_speed)

        self.step()

    def start_tank(self, left_speed, right_speed) :
        """ Activate both motors
        ---
        left_speed (int)  : Left motor speed
        right_speed (int) : Right motor speed
        """

        if not isinstance(left_speed, int) :
            raise TypeError('left_speed is not an integer')
        if not isinstance(right_speed, int) :
            raise TypeError('right_speed is not an integer')

        left_speed = min(max(left_speed,- self.s_max_speed),self.s_max_speed)
        right_speed = min(max(right_speed,- self.s_max_speed),self.s_max_speed)

        self.step()

    def start_at_power(self, power, steering=0) :
        """ Activate both motors
        ---
        steering (int)  : Direction and quantity to orient the base
        power (int)     : Displacement power
        """

        if not isinstance(steering, int) :
            raise TypeError('steering is not an integer')
        if not isinstance(power, int) :
            raise TypeError('power is not an integer')

        power = min(max(power,- self.s_max_power),self.s_max_power)
        steering = min(max(steering,- self.s_max_steering),self.s_max_steering)

        self.step()

    def start_tank_at_power(self, left_power, right_power) :
        """ Activate both motors
        ---
        left_speed (int)  : Left motor speed
        right_speed (int) : Right motor speed
        """

        if not isinstance(left_power, int) :
            raise TypeError('left_power is not an integer')
        if not isinstance(right_power, int) :
            raise TypeError('right_power is not an integer')

        left_power = min(max(left_power,- self.s_max_power),self.s_max_power)
        right_power = min(max(right_power,- self.s_max_power),self.s_max_power)

        self.step()

    def get_default_speed(self) :
        """ Return default speed
        ---
        returns (int) : Default speed when not specified
        """
        return self.m_default_speed

    def set_motor_rotation(self, amount, unit='cm') :
        """ Set the distance reached by the motors when a motor rotation happens
        ---
        amount (float)  : Displacement value
        unit (str)      : Displacement unit
        """

        if not isinstance(amount, (float, int)) :
            raise TypeError('amount is not a number')
        if not isinstance(unit, str) :
            raise TypeError('unit is not a string')

        if unit not in ['cm', 'inches'] :
            raise ValueError('unit is not one of the allowed values')

    def set_default_speed(self, speed) :
        """ Set the motorpair default speed
        ---
        A displacement method should be called for this value to be taken into account
        ---
        speed (int)  : Default speed
        """

        if not isinstance(speed, int) :
            raise TypeError('speed is not a number')

        self.m_default_speed = speed

    def set_stop_action(self, action) :
        """ Sets the action to be performed on stop
        ---
        action (str) : One of coast, brake or hold
        """
        if not isinstance(action, str) :
            raise TypeError('action is not a string')

        if action not in motor_stop_actions :
            raise ValueError('action is not one of the allowed values')

        self.m_stop_action = action

# ----------------- SIMULATION FUNCTIONS -----------------

    def step(self) :
        """ Step to the next simulation step """

        left_degrees          = int(round(self.m_scenario['left degrees'][self.m_current_step]))
        right_degrees         = int(round(self.m_scenario['right degrees'][self.m_current_step]))

        self.m_left_motor.set_degrees(left_degrees)
        self.m_right_motor.set_degrees(right_degrees)

        super().step()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'left degrees' in columns :
            raise Exception('Missing "left degrees" in ' + str(columns) + ' dictionary')
        if not 'right degrees' in columns :
            raise Exception('Missing "right degrees" in ' + str(columns) + ' dictionary')
# pylint: enable=R0902
