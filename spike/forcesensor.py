""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Force sensor mock
# -------------------------------------------------------
# Nadège LEMPERIERE,  @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """


# Standard includes
from time import sleep

# Local includes
from spike.mock     import Mock
from spike.truth    import Truth

class ForceSensor(Mock) :
    """ Force Sensor mocking function """

    m_force                     = 0

    s_force_for_being_pressed   = 2
    s_max_force                 = 10

# ------------ SPIKE FORCE SENSOR FUNCTIONS --------------

# pylint: disable=W0102
    def __init__(self, port) :
        """ Contructor
        ---
        port (str)      : The port on which the sensor is located
        """

        super().__init__()

        self.m_shared_truth   = Truth()
        check_for_component = self.m_shared_truth.check_component(port, 'ForceSensor')
        if  not check_for_component :
            raise ValueError('Port ' + port + ' does not host a force sensor')
        self.m_shared_truth.register_component(port, self)

        self.m_force            = 0
        self.s_default_columns  = {
            'force':'force',
        }
        self.columns()

# pylint: enable=W0102

    def wait_until_pressed(self) :
        """ Wait until the sensor is pressed"""

        while self.m_force < self.s_force_for_being_pressed :
            sleep(0.01)

    def wait_until_released(self) :
        """ Wait until the sensor is released"""

        while self.m_force >= self.s_force_for_being_pressed :
            sleep(0.01)

    def is_pressed(self) :
        """ Return current status
        ---
        returns (bool)  : True if the sensor is pressed, False otherwise
        """
        return self.m_force >= self.s_force_for_being_pressed

    def get_force_newton(self) :
        """ Return force in newtons"""
        return self.m_force

    def get_force_percentage(self) :
        """ Return force in percentage of maximal force"""
        return int(round(self.m_force * 100 / self.s_max_force))

# ----------------- SIMULATION FUNCTIONS -----------------

    def update(self) :
        """ Step to the next simulation step """

        self.m_force = self.m_shared_context.get_data(self.m_columns['force'])

        super().update()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'force' in columns :
            raise Exception('Missing "force" in ' + str(columns) + ' dictionary')
