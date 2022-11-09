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

# Constants
motor_directions = [
    'shortest path',
    'clockwise',
    'counterclockwise',
]
motor_stop_actions = [
    'coast',
    'hold',
    'brake',
]

# pylint: disable=R0902
class Motor(Mock) :
    """ Motor mocking function """

    m_default_speed             = 100
    m_stop_action               = 'brake'
    m_speed                     = 0
    m_position                  = 0
    m_degrees                   = 0
    m_position                  = 0
    m_delta_degrees             = 0
    m_shared_robot              = None

    m_was_interrupted           = False
    m_was_stalled               = False
    m_shall_stop_when_stalled   = False

    s_max_speed                 = 100
    s_max_steering              = 100
    s_max_power                 = 100

# ---------------- SPIKE MOTOR FUNCTIONS -----------------

    def __init__(self, port) :
        """ Contructor
        ---
        port (str)      : The port on which the motor is located
        """

        super().__init__()
        self.m_shared_robot      = Robot()

        if  self.m_shared_robot.get_component(port) is None or \
            self.m_shared_robot.get_component(port) != 'Motor' :
            raise ValueError('Port ' + port + ' does not host a motor')

        self.m_default_speed            = 100
        self.m_stop_action              = 'brake'
        self.m_speed                    = 0
        self.m_position                 = 0
        self.m_degrees                  = 0
        self.m_delta_degrees            = 0
        self.s_default_columns  = {
            'degrees':'degrees',
        }
        self.m_position                 = 0

        self.m_was_interrupted          = False
        self.m_was_stalled              = False
        self.m_shall_stop_when_stalled  = False

        self.m_shared_robot.register_component(port, self)

    def run_to_position(self, degrees, direction='shortest path', speed=None) :
        """ Runs the motor to an absolute position.
        ---
        degrees (int)    : Number of degrees motor shall make
        direction (str)  : Motor rotation direction
        speed (int)      : Displacement speed
        """

        if speed is None : speed = self.m_default_speed

        if not isinstance(degrees, int) :
            raise TypeError('degrees is not an integer')
        if not isinstance(direction, str) :
            raise TypeError('direction is not a string')
        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        if direction not in motor_directions :
            raise ValueError('direction is not one of the allowed values')
        if degrees < 0 or degrees >= 360 :
            raise ValueError('degrees is not in the range 0-359')


        if speed < - self.s_max_speed : speed = - self.s_max_speed
        if speed > self.s_max_speed :   speed = self.s_max_speed

    def run_to_degrees_counted(self, degrees, speed=None):
        """ Runs the motor until the number of degrees counted
        is equal to the value that has been specified by the "degrees" parameter.
        ---
        degrees (int)  : Number of degrees motor shall make
        speed (int)    : Displacement speed
        """

        if speed is None : speed = self.m_default_speed

        if not isinstance(degrees, int) :
            raise TypeError('degrees is not an integer')
        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        if speed < - self.s_max_speed : speed = - self.s_max_speed
        if speed > self.s_max_speed :   speed = self.s_max_speed

    def run_for_degrees(self, degrees, speed=None):
        """ Runs the motor for a specified number of degrees.
        ---
        degrees (int)  : Number of degrees motor shall make
        speed (int)    : Displacement speed
        """

        if speed is None : speed = self.m_default_speed

        if not isinstance(degrees, int) :
            raise TypeError('degrees is not an integer')
        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        if speed < - self.s_max_speed : speed = - self.s_max_speed
        if speed > self.s_max_speed :   speed = self.s_max_speed

    def run_for_rotations(self, rotations, speed=None):
        """ Runs the motor for a specified number of rotations.
        ---
        rotations (float) : Number of rotations motor shall make
        speed (int)       : Displacement speed
        """

        if speed is None : speed = self.m_default_speed

        if not isinstance(rotations, (float, int)) :
            raise TypeError('rotations is not a number')
        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        if speed < - self.s_max_speed : speed = - self.s_max_speed
        if speed > self.s_max_speed :   speed = self.s_max_speed

    def run_for_seconds(self, seconds, speed=None):
        """ Runs the motor for a specified number of seconds.
        ---
        seconds (float) : Number of seconds motor during which motor shall run
        speed (int)     : Displacement speed
        """

        if speed is None : speed = self.m_default_speed

        if not isinstance(seconds, (float, int)) :
            raise TypeError('seconds is not a number')
        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        if speed < - self.s_max_speed : speed = - self.s_max_speed
        if speed > self.s_max_speed :   speed = self.s_max_speed

    def start(self, speed=None) :
        """ Activate motor
        ---
        speed (int)     : Rotation speed
        """

        if speed is None : speed = self.m_default_speed

        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        if speed < - self.s_max_speed : speed = - self.s_max_speed
        if speed > self.s_max_speed :   speed = self.s_max_speed

    def stop(self) :
        """ Stop base """

    def start_at_power(self, power) :
        """ Activate motors
        ---
        power (int)     : Displacement power
        """

        if not isinstance(power, int) :
            raise TypeError('power is not an integer')

        if power < - self.s_max_power : power = - self.s_max_power
        if power > self.s_max_power :   power = self.s_max_power

    def get_speed(self) :
        """ Return current speed
        ---
        returns (int) : Current speed
        """
        return self.m_speed

    def get_position(self) :
        """ Retrieves the motor position. This is the clockwise angle between
        the moving marker and the zero-point marker on the motor.
        ---
        returns (int) : Current position
        """
        return self.m_position

    def get_degrees_counted(self) :
        """ Retrieves the number of degrees that have been counted by the motor.
        ---
        returns (int) : Current counted degrees
        """
        return self.m_degrees - self.m_delta_degrees

    def get_default_speed(self) :
        """ Return default speed
        ---
        returns (int) : Default speed when not specified
        """
        return self.m_default_speed

    def was_interrupted(self) :
        """ Tests whether the motor was interrupted.
        ---
        returns (bool) : True if the motor has been interrupted
        since last call, False otherwise
        """
        result = self.m_was_interrupted
        self.m_was_interrupted = False
        return result

    def was_stalled(self) :
        """ Tests whether the motor was stalled.
        ---
        returns (bool) : True if the motor has been stalled
        since last call, False otherwise
        """
        result = self.m_was_stalled
        self.m_was_stalled = False
        return result

    def set_default_speed(self, speed) :
        """ Set the motor default speed
        ---
        A displacement method should be called for this value to be taken into account
        ---
        speed (int)  : Default speed
        """

        if not isinstance(speed, int) :
            raise TypeError('speed is not an integer')

        self.m_default_speed = speed

    def set_degrees_counted(self, degrees_counted) :
        """ Reinitialize the motors degrees
        ---
        degrees_counted (int)  : New degrees value
        """

        if not isinstance(degrees_counted, int) :
            raise TypeError('degrees_counted is not an integer')

        self.m_delta_degrees = self.m_degrees - degrees_counted

    def set_stall_detection(self, stop_when_stalled) :
        """ Sets the action to be performed on stop
        ---
        action (str) : One of coast, brake or hold
        """
        if not isinstance(stop_when_stalled, bool) :
            raise TypeError('stop_when_stalled is not a boolean')


        self.m_shall_stop_when_stalled = stop_when_stalled

# pylint: disable=R0801
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
# pylint: enable=R0801
# pylint: enable=R0902

# ----------------- SIMULATION FUNCTIONS -----------------

    def step(self) :
        """ Step to the next simulation step """

        self.m_degrees          = int(round(self.m_scenario['degrees'][self.m_current_step]))
        self.m_position         = (self.m_degrees) % 360

        super().step()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'degrees' in columns :
            raise Exception('Missing "degrees" in ' + str(columns) + ' dictionary')

    def set_degrees(self, degrees) :
        """ Set the degree number from another mock
        ---
        degrees (float) : The degrees to set as counted in motor
        """
        self.m_degrees          = int(round(degrees))
        self.m_position         = (self.m_degrees) % 360


# pylint: enable=R0902
