""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# High resolution timer with a milliseconds resolution
# emulating spike timer interfaces on standard python
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# System includes
from time import sleep
from inspect import signature

# Local includes
from spike.mock import Mock

# pylint: disable=C0103
def equal_to(a, b) :
    """ Default function for wait_until function """
    return a == b
# pylint: enable=C0103

class TimerSingleton(Mock) :
    """ Singleton containing synthetic data shared by all timers """

    m_time           = 0

# pylint: disable=W0102
    def __new__(cls):

        if not hasattr(cls, 'instance'):
            cls.instance = super(TimerSingleton, cls).__new__(cls)
        return cls.instance

    def __init__(self) :
        """ Contructor """
        if len(self.m_scenario) == 0 :
            super().__init__()
            self.m_time             = 0

        self.s_default_columns  = {
            'time' : 'time',
        }

# ----------------- SIMULATION FUNCTIONS -----------------

    def step(self) :
        """ Step to the next simulation step """

        self.m_time         = self.m_scenario['time'][self.m_current_step]
        super().step()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'time' in columns :
            raise Exception('Missing "time" in ' + str(columns) + ' dictionary')


# pylint: enable=W0102

class Timer() :
    """ Timer"""

    m_reference_time    = -1
    m_common_timer      = None

    def __init__(self) :
        """ Contructor """
        self.m_reference_time    = -1
        self.m_common_timer = TimerSingleton()

    def now(self) :
        """ Current time return function
        ---
        returns (float) : the time in seconds """

        return self.m_common_timer.m_time - self.m_reference_time

    def reset(self) :
        """ Time reset function """
        self.m_reference_time = self.m_common_timer.m_time

def wait_for_seconds(seconds) :
    """ Stop the processing for a given amount of time
    ---
    seconds (float)    : Beep duration in seconds
    """

    if not isinstance(seconds, (float, int)):
        raise TypeError('seconds is not a number')
    if seconds < 0 :
        raise ValueError('seconds is not at least 0')

    common_timer    = TimerSingleton()
    reference_time  = common_timer.m_time
    while (common_timer.m_time - reference_time) < seconds :
        sleep(0.01)

def wait_until(get_value_function, operator_function=equal_to, target_value=True) :
    """ Waits until the condition is true before continuing with the program.
    ---
    get_value_function (callable)   : A function that returns the current value to be
    compared to the target value.
    operator_function (callable)    : A function that compares two arguments. The first
    argument will be the result of get_value_function(), and the second argument will be
    target_value. The function will compare both values and return the result.
    target_value     (any type)     : Any object that can be compared by operator_function.
    """

    if not callable(get_value_function) :
        raise TypeError('get_value_function is not callable')
    if not callable(operator_function) :
        raise TypeError('operator_function is not callable')

    sgn =  signature(operator_function)
    print(str(sgn))

    current = get_value_function()
    while not operator_function(current, target_value) :
        sleep(0.01)
