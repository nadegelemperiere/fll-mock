""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Hub speaker mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# System includes
from time import sleep

# Local includes
from spike.mock import Mock

class Speaker(Mock) :
    """ Hub speaker mocking function """

    m_is_beeping    = False
    m_note          = 0
    m_volume        = 0
    m_time          = 0

    s_max_volume    = 100
    s_min_note      = 44
    s_max_note      = 123


# ------------ SPIKE LIGHT MATRIX FUNCTIONS --------------

# pylint: disable=W0102
    def __init__(self) :
        """ Contructor
        ---
        columns  (dict)   : The excel simulation data column name
        """

        super().__init__()
        self.m_is_beeping   = False
        self.m_note         = 0
        self.m_volume       = 0
        self.m_time         = 0
        self.s_default_columns = {
            'time' : 'time',
        }

# pylint: enable=W0102

    def beep(self, note=60, seconds=0.2) :
        """ Plays a beep on the Hub.
        ---
        note (float)       : The MIDI note number
        seconds (float)    : Beep duration in seconds
        """

        if not isinstance(note, (float, int)):
            raise TypeError('note is not a number')
        if not isinstance(seconds, float) and not isinstance(seconds, int):
            raise TypeError('seconds is not a number')

        if note < self.s_min_note or note > self.s_max_note :
            raise ValueError('note is not within the allowed range of 44-123')

        self.m_is_beeping = True
        self.m_note       = note
        current_time = self.m_time
        while self.m_time - current_time < seconds :
            sleep(0.01)
        self.m_is_beeping = False
        self.m_note       = 0

    def start_beep(self, note=60) :
        """ Plays a beep on the Hub.
        ---
        note (float)       : The MIDI note number
        """

        if not isinstance(note, (float, int)):
            raise TypeError('note is not a number')

        if note < 44 or note > 123 :
            raise ValueError('note is not within the allowed range of 44-123')

        self.m_is_beeping = True
        self.m_note       = note

    def stop(self) :
        """ Beep stopping function """
        self.m_is_beeping = False
        self.m_note       = 0

    def get_volume(self) :
        """ Volume return function
        ---
        returns (int) : The speaker volume
        """
        return self.m_volume

    def set_volume(self, volume) :
        """ Volume setting function
        ---
        volume (int) : The speaker volume
        """

        if not isinstance(volume, int):
            raise TypeError('volume is not an integer')

        self.m_volume = volume
        self.m_volume = min(max(0,self.m_volume),self.s_max_volume)

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
