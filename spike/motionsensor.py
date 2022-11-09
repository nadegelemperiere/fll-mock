""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Hub motion sensor mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# System includes
from time import sleep

# Local includes
from spike.mock import Mock

# Constants
motionsensor_gestures = [
    'shaken',
    'tapped',
    'doubletapped',
    'falling',
]

# pylint: disable=R0902
class MotionSensor(Mock) :
    """ Color sensor mocking function """

    m_yaw               = 0
    m_pitch             = 0
    m_roll              = 0
    m_gesture           = ''

    m_zero_yaw_angle    = 0
    m_last_gesture      = ''
    m_was_gesture       = {}

# ------------ SPIKE COLOR SENSOR FUNCTIONS --------------

# pylint: disable=W0102
    def __init__(self) :
        """ Contructor """

        super().__init__()

        self.m_yaw               = 0
        self.m_pitch             = 0
        self.m_roll              = 0
        self.m_gesture           = ''
        self.s_default_columns  = {
            'yaw':'yaw',
            'pitch':'pitch',
            'roll':'roll',
            'gesture':'gesture',
            'time' : 'time',
        }
        self.m_commands['time'] = []
        self.m_commands['command'] = []

        self.m_zero_yaw_angle    = 0
        self.m_last_gesture      = ''
        for gesture in motionsensor_gestures :
            self.m_was_gesture[gesture] = False
        self.m_was_gesture['none'] = True

        self.m_wait_gesture = False

# pylint: enable=W0102

    def get_roll_angle(self) :
        """ Return current roll angle
        ---
        returns (int)   : Roll angle in degrees (positive to the right)
        """
        return self.m_roll

    def get_pitch_angle(self) :
        """ Return current pitch angle
        ---
        returns (int)   : Pitch angle in degrees (positive to the right)
        """
        return self.m_pitch

    def get_yaw_angle(self) :
        """ Return current yaw angle
        ---
        returns (int)   : Yaw angle in degrees (positive to the right)
        """
        return self.m_yaw - self.m_zero_yaw_angle

    def reset_yaw_angle(self) :
        """ Reset reference yaw angle
        """
        self.m_commands['command'][-1] = 'reset_yaw_angle'
        self.m_zero_yaw_angle = self.m_yaw

    def get_gesture(self) :
        """ Return most recent gesture
        ---
        returns (str)   : Gesture name ('shaken','tapped','doubletapped','falling')
        """
        return self.m_last_gesture

    def was_gesture(self, gesture) :
        """ Test if the gesture happened since last call to this function
        ---
        gesture (str)   : Gesture to look for
        ---
        returns (str)   : True if the gesture occured, false otherwise
        """
        if gesture not in motionsensor_gestures :
            if gesture != 'none' :
                raise ValueError('Invalid gesture : ' + gesture)

        result = self.m_was_gesture[gesture]

        for ges in motionsensor_gestures :
            self.m_was_gesture[ges] = False
        self.m_was_gesture['none'] = True

        return result

    def get_orientation(self) :
        """ Return hub orientation
        ---
        returns (str)   : Hub orientation ('front','back','up','down','leftside','rightside')
        """

        # random value : to be confirmed by test
        result = ''
        if self.m_pitch > 10 : result = 'up'
        elif self.m_pitch < -10 : result = 'down'
        elif self.m_yaw > -45 and self.m_yaw <= 45      : result = 'front'
        elif self.m_yaw > 45 and self.m_yaw <= 135      : result = 'rightside'
        elif self.m_yaw > -135 and self.m_yaw <= -45    : result = 'leftside'
        elif self.m_yaw > 135 or self.m_yaw <= -135     : result = 'back'

        return result

    def wait_for_new_gesture(self) :
        """ Wait until the hub is in a new gesture """

        current_gesture = self.m_last_gesture
        while current_gesture == self.m_last_gesture :
            sleep(0.01)

    def wait_for_new_orientation(self) :
        """ Wait until the hub gets a new orientation """

        current_orientation = self.get_orientation()
        while current_orientation == self.get_orientation() :
            sleep(0.01)

# ----------------- SIMULATION FUNCTIONS -----------------

    def step(self) :
        """ Step to the next simulation step """

        self.m_yaw          = int(self.m_scenario['yaw'][self.m_current_step])
        self.m_roll         = int(self.m_scenario['roll'][self.m_current_step])
        self.m_pitch        = int(self.m_scenario['pitch'][self.m_current_step])

        gesture = self.m_scenario['gesture'][self.m_current_step]
        if gesture in motionsensor_gestures :
            self.m_gesture = gesture
            self.m_last_gesture  = gesture
            self.m_was_gesture[gesture] = True
            self.m_was_gesture['none'] = False
        elif gesture is None:
            self.m_gesture = ''
        else :
            raise ValueError('Invalid gesture : ' + gesture)

        self.m_commands['time'].append(self.m_scenario['time'][self.m_current_step])
        self.m_commands['command'].append(None)

        super().step()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'roll' in columns :
            raise Exception('Missing "roll" in ' + str(columns) + ' dictionary')
        if not 'pitch' in columns :
            raise Exception('Missing "pitch" in ' + str(columns) + ' dictionary')
        if not 'yaw' in columns :
            raise Exception('Missing "yaw" in ' + str(columns) + ' dictionary')
        if not 'gesture' in columns :
            raise Exception('Missing "gesture" in ' + str(columns) + ' dictionary')
# pylint: enable=R0902
