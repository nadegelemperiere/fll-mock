""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Hub button mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# Standard includes
from time import sleep

# Local includes
from spike.mock import Mock

# Constants

class Button(Mock) :
    """ Hub button mocking function """

    m_is_pressed    = False
    m_was_pressed   = False

# --------------- SPIKE BUTTON FUNCTIONS -----------------

# pylint: disable=W0102
    def __init__(self) :
        """ Contructor """

        super().__init__()

        self.m_is_pressed       = False
        self.m_was_pressed      = False
        self.s_default_columns  = {
            'is_pressed':'is_pressed',
        }
# pylint: enable=W0102

    def wait_until_pressed(self) :
        """ Wait until the button is pressed"""

        while not self.m_is_pressed :
            sleep(0.01)

    def wait_until_released(self) :
        """ Wait until the button is released"""

        while self.m_is_pressed :
            sleep(0.01)

    def was_pressed(self) :
        """Check if the button was pressed until last call
        ---
        returns (bool)  : True if was pressed until last call to this function, false otherwise
        """

        result = self.m_was_pressed
        self.m_was_pressed = False

        return result

    def is_pressed(self) :
        """ Return current status
        ---
        returns (bool)  : True if the button is pressed, False otherwise
        """
        return self.m_is_pressed

# ----------------- SIMULATION FUNCTIONS -----------------

    def step(self) :
        """ Step to the next simulation step """

        self.m_is_pressed   = self.m_scenario['is_pressed'][self.m_current_step]
        if not self.m_was_pressed :
            self.m_was_pressed = self.m_scenario['is_pressed'][self.m_current_step]

        super().step()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'is_pressed' in columns :
            raise Exception('Missing "is_pressed" in ' + str(columns) + ' dictionary')
