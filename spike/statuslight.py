""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Hub status_light mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# Local includes
from spike.mock import Mock

# Constants
status_light_colors = [
    'azure','black','blue','cyan','green','orange','pink','red','violet','yellow','white',
]

class StatusLight(Mock) :
    """ Hub status_light mocking function """

    m_color = ''
    m_is_on = False

# ------------ SPIKE LIGHT MATRIX FUNCTIONS --------------

# pylint: disable=W0102
    def __init__(self) :
        """ Contructor """

        super().__init__()
        self.m_color   = 'white'
        self.m_is_on   = False
        self.s_default_columns = {
            'time' : 'time',
        }
        self.columns()

# pylint: enable=W0102

# pylint: disable=C0103
    def on(self, color='white') :
        """ Sets the color of the light
        ---
        color (str)       : The light color
        """

        if not isinstance(color, str) :
            raise TypeError('color is not a string')

        if color not in status_light_colors :
            raise ValueError('color is not one of the allowed values')

        self.m_shared_context.log_command('on',{
            'color'    : color,
        })

        self.m_color = color
        self.m_is_on = True
# pylint: enable=C0103

    def off(self) :
        """ Turns off the light"""

        self.m_shared_context.log_command('off',{})

        self.m_is_on = False

# ----------------- SIMULATION FUNCTIONS -----------------

# pylint: disable=W0246
    def update(self) :
        """ Step to the next simulation step """

        super().update()
# pylint: enable=W0246

    def get_color(self) :
        """ Return color """
        return self.m_color

    def get_status(self) :
        """ Return True if on, false otherwise """
        return self.m_is_on
