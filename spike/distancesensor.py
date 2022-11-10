""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Distance sensor mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# System includes
from time import sleep

# Local includes
from spike.mock     import Mock
from spike.truth    import Truth

# pylint: disable=R0902
class DistanceSensor(Mock) :
    """ Distance sensor mocking function """

    m_right_top                 = 100
    m_left_top                  = 100
    m_right_bottom              = 100
    m_left_bottom               = 100

    m_distance                  = 0

    s_cm_to_inches              = 0.39370079
    s_max_distance              = 200
    s_max_distance_short_range  = 50

# ---------- SPIKE DISTANCE SENSOR FUNCTIONS -------------

# pylint: disable=W0102
    def __init__(self, port) :
        """ Contructor
        ---
        port (str)      : The port on which the sensor is located
        """

        super().__init__()


        self.m_shared_truth   = Truth()
        check_for_component = self.m_shared_truth.check_component(port, 'DistanceSensor')
        if  not check_for_component :
            raise ValueError('Port ' + port + ' does not host a distance sensor')
        self.m_shared_truth.register_component(port, self)

        self.m_right_top     = 100
        self.m_left_top      = 100
        self.m_right_bottom  = 100
        self.m_left_bottom   = 100
        self.m_distance      = 0
        self.s_default_columns  = {
            'distance':'distance',
            'time' : 'time',
        }
        self.m_commands['time']         = []
        self.m_commands['command']      = []
        self.m_commands['right_top']    = []
        self.m_commands['left_top']     = []
        self.m_commands['right_bottom'] = []
        self.m_commands['left_bottom']  = []


# pylint: enable=W0102

    def get_distance_cm(self, short_range=False) :
        """ Distance return function
        ---
        short_range     : True to make a more precise measurement
        of a closest object, False otherwise
        ---
        returns (float) : distance to closest object in centimers
        """

        result = None

        if not isinstance(short_range, bool) :
            raise TypeError('short_range is not a boolean')
        if self.m_distance < self.s_max_distance and not short_range :
            result = self.m_distance
        elif self.m_distance < self.s_max_distance_short_range and short_range :
            result = self.m_distance

        return result

    def get_distance_inches(self, short_range=False) :
        """ Distance return function
        ---
        short_range     : True to make a more precise measurement
        of a closest object, False otherwise
        ---
        returns (float) : distance to closest object in inches
        """

        result = self.get_distance_cm(short_range)
        if result is not None : result = round(result * self.s_cm_to_inches)

        return result

    def get_distance_percentage(self, short_range=False) :
        """ Distance return function
        ---
        short_range     : True to make a more precise measurement
        of a closest object, False otherwise
        ---
        returns (float) : distance to closest object in percentage
        """

        result = self.get_distance_cm(short_range)
        if result is not None : result = int(result / self.s_max_distance * 100)

        return result

    def wait_for_distance_farther_than(self,distance, unit='cm', short_range=False) :
        """ Wait until a the measured distance is greater than a value
        ---
        distance        : Distance threshold
        unit            : Distance measurement unit
        short_range     : True to make a more precise measurement
        of a closest object, False otherwise
        ---
        returns (str)   : The current color on first call, then the new color
        """


        measure = self.s_max_distance
        if unit == 'cm'     : measure = self.get_distance_cm(short_range)
        if unit == 'inch'   : measure = self.get_distance_inches(short_range)
        if unit == '%'      : measure = self.get_distance_percentage(short_range)
        if measure is None  : measure = 100000
        while measure < distance :
            sleep(0.01)
            measure = self.s_max_distance
            if unit == 'cm'     : measure = self.get_distance_cm(short_range)
            if unit == 'inch'   : measure = self.get_distance_inches(short_range)
            if unit == '%'      : measure = self.get_distance_percentage(short_range)
            if measure is None  : measure = 100000

    def wait_for_distance_closer_than(self,distance, unit='cm', short_range=False) :
        """ Wait until a the measured distance is closer than a value
        ---
        distance        : Distance threshold
        unit            : Distance measurement unit
        short_range     : True to make a more precise measurement
        of a closest object, False otherwise
        ---
        returns (str)   : The current color on first call, then the new color
        """

        measure = None
        if unit == 'cm'     : measure = self.get_distance_cm(short_range)
        if unit == 'inch'   : measure = self.get_distance_inches(short_range)
        if unit == '%'      : measure = self.get_distance_percentage(short_range)
        if measure is None  : measure = 100000
        while measure > distance :
            sleep(0.01)
            measure = None
            if unit == 'cm'     : measure = self.get_distance_cm(short_range)
            if unit == 'inch'   : measure = self.get_distance_inches(short_range)
            if unit == '%'      : measure = self.get_distance_percentage(short_range)
            if measure is None  : measure = 100000

    def light_up_all(self, brightness=100) :
        """ Light all distance sensor LEDs
        ---
        brightness (int)    : Required LED brightness (0-100)
        ---
        TypeError           : brightness is not an integer
        """

        if not isinstance(brightness,int) :
            raise TypeError('brightness is not an integer')

        self.m_right_top    = max(0,min(abs(brightness),100))
        self.m_left_top     = max(0,min(abs(brightness),100))
        self.m_right_bottom = max(0,min(abs(brightness),100))
        self.m_left_bottom  = max(0,min(abs(brightness),100))

        self.m_commands['command'][-1]      = 'light_up_all'
        self.m_commands['right_top'][-1]    = self.m_right_top
        self.m_commands['left_top'][-1]     = self.m_left_top
        self.m_commands['right_bottom'][-1] = self.m_right_bottom
        self.m_commands['left_bottom'][-1]  = self.m_left_bottom

    def light_up(self, right_top, left_top, right_bottom, left_bottom) :
        """ Light all color sensor LEDs
        ---
        right_top (int)     : Required right top LED brightness (0-100)
        left_top (int)      : Required left top LED brightness (0-100)
        right_bottom (int)  : Required right bottom LED brightness (0-100)
        left_bottom (int)   : Required left bottom LED brightness (0-100)
        ---
        TypeError           : brightness is not an integer
        """

        if not isinstance(right_top, int) :
            raise TypeError('right_top is not an integer')
        if not isinstance(left_top, int) :
            raise TypeError('left_top is not an integer')
        if not isinstance(right_bottom, int) :
            raise TypeError('right_bottom is not an integer')
        if not isinstance(left_bottom, int) :
            raise TypeError('left_bottom is not an integer')

        self.m_right_top = max(0,min(abs(right_top),100))
        self.m_left_top = max(0,min(abs(left_top),100))
        self.m_right_bottom = max(0,min(abs(right_bottom),100))
        self.m_left_bottom = max(0,min(abs(left_bottom),100))

        self.m_commands['command'][-1]      = 'light_up'
        self.m_commands['right_top'][-1]    = self.m_right_top
        self.m_commands['left_top'][-1]     = self.m_left_top
        self.m_commands['right_bottom'][-1] = self.m_right_bottom
        self.m_commands['left_bottom'][-1]  = self.m_left_bottom

# ----------------- SIMULATION FUNCTIONS -----------------

    def step(self) :
        """ Step to the next simulation step """

        self.m_distance = int(self.m_scenario['distance'][self.m_current_step])

        self.m_commands['time'].append(self.m_scenario['time'][self.m_current_step])
        self.m_commands['command'].append(None)
        self.m_commands['right_top'].append(None)
        self.m_commands['left_top'].append(None)
        self.m_commands['right_bottom'].append(None)
        self.m_commands['left_bottom'].append(None)

        super().step()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'distance' in columns :
            raise Exception('Missing "distance" in ' + str(columns) + ' dictionary')
