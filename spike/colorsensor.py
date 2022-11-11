""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Hub button mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# System includes
from time import sleep

# Webcolors includes
from webcolors import rgb_to_name

# Local includes
from spike.mock     import Mock
from spike.truth    import Truth

# Constants
css3_to_spike_colormap = {
    'lime' : 'green',
    'red' : 'red',
    'blue' : 'blue',
    'green' : 'green',
    'white' : 'white',
    'black' : 'black',
}

# pylint: disable=R0902
class ColorSensor(Mock) :
    """ Color sensor mocking function """

    m_blue              = 0
    m_green             = 0
    m_red               = 0
    m_color             = None
    m_reflected         = 0
    m_ambiant           = 0

    m_previous_color    = ''
    m_light1            = 100
    m_light2            = 100
    m_light3            = 100


# ------------ SPIKE COLOR SENSOR FUNCTIONS --------------

# pylint: disable=W0102
    def __init__(self, port) :
        """ Contructor
        ---
        port (str)      : The port on which the sensor is located
        """

        super().__init__()

        self.m_shared_truth   = Truth()
        check_for_component = self.m_shared_truth.check_component(port, 'ColorSensor')
        if  not check_for_component :
            raise ValueError('Port ' + port + ' does not host a color sensor')
        self.m_shared_truth.register_component(port, self)

        self.m_light1           = 100
        self.m_light2           = 100
        self.m_light3           = 100
        self.m_brightness       = 0
        self.s_default_columns  = {
            'red':'red',
            'green':'green',
            'blue':'blue',
            'reflected':'reflected',
            'ambiant':'ambiant',
            'time' : 'time',
        }
        self.columns()


# pylint: enable=W0102

    def get_color(self) :
        """ Return current color
        ---
        returns (str)   : The name of the current color sensed
        """
        return self.m_color

    def get_ambiant_light(self) :
        """ Return current ambiant light intensity
        ---
        returns (int)  : The intensity of the ambiant light (0-100)
        """
        return self.m_ambiant

    def get_reflected_light(self) :
        """ Return current reflected light intensity
        ---
        returns (int)  : The intensity of the reflected light (0-100)
        """
        return self.m_reflected

    def get_rgb_intensity(self) :
        """ Return intensity tuple
        ---
        returns (tuple) : red, green, blue and global itensity
        """

        result = (  self.m_red , \
                    self.m_green , \
                    self.m_blue , \
                    (self.m_red + self.m_green + self.m_blue) / 3)

        return result

    def get_red(self) :
        """ Return current red color intensity
        ---
        returns (int)  : The intensity of the red color (0-1024)
        """
        return self.m_red

    def get_green(self) :
        """ Return current green color intensity
        ---
        returns (int)  : The intensity of the green color (0-1024)
        """
        return self.m_green

    def get_blue(self) :
        """ Return current blue color intensity
        ---
        returns (int)  : The intensity of the blue color (0-1024)
        """
        return self.m_blue

    def wait_until_color(self, color) :
        """ Wait until color is detected
        ---
        color (str)    : Color to look for
        """

        while self.m_color != color :
            sleep(0.01)

    def wait_for_new_color(self) :
        """ Wait until a new color is detected
        ---
        returns (str)   : The current color on first call, then the new color
        """

        result = ''

        if self.m_previous_color == '' :
            self.m_previous_color = self.m_color
            result = self.m_previous_color
        else :
            while self.m_color == self.m_previous_color :
                sleep(0.01)
            result = self.m_color
            self.m_previous_color = ''

        return result

    def light_up_all(self, brightness=100) :
        """ Light all color sensor LEDs
        ---
        brightness (int)    :  Required LED brightness (0-100)
        ---
        TypeError           : Brightness is not an integer
        """

        if not isinstance(brightness,int) :
            raise TypeError('brightness is not an integer')

        self.m_light1 = max(0,min(abs(brightness),100))
        self.m_light2 = max(0,min(abs(brightness),100))
        self.m_light3 = max(0,min(abs(brightness),100))

        self.m_shared_context.log_command('light_up_all',{
            'light1' : self.m_light1,
            'light2' : self.m_light2,
            'light3' : self.m_light3
        })

    def light_up(self, light_1, light_2, light_3) :
        """ Light all color sensor LEDs
        ---
        light_1 (int)   : Required first LED brightness (0-100)
        light_2 (int)   : Required second LED brightness (0-100)
        light_3 (int)   : Required third LED brightness (0-100)
        ---
        TypeError       : Brightness is not an integer
        """

        if not isinstance(light_1, int) :
            raise TypeError('light_1 is not an integer')
        if not isinstance(light_2, int) :
            raise TypeError('light_2 is not an integer')
        if not isinstance(light_3, int) :
            raise TypeError('light_3 is not an integer')

        self.m_light1 = max(0,min(abs(light_1),100))
        self.m_light2 = max(0,min(abs(light_2),100))
        self.m_light3 = max(0,min(abs(light_3),100))

        self.m_shared_context.log_command('light_up',{
            'light1' : self.m_light1,
            'light2' : self.m_light2,
            'light3' : self.m_light3
        })

# ----------------- SIMULATION FUNCTIONS -----------------

    def update(self) :
        """ Step to the next simulation step """

        light_ratio      = (self.m_light1 + self.m_light2 + self.m_light3) / 300
        self.m_red       = int(self.m_shared_context.get_data(self.m_columns['red']) * light_ratio)
        self.m_green     = int(self.m_shared_context.get_data(self.m_columns['green'])* light_ratio)
        self.m_blue      = int(self.m_shared_context.get_data(self.m_columns['blue']) * light_ratio)
        self.m_reflected = int(
            self.m_shared_context.get_data(self.m_columns['reflected']) * light_ratio)
        self.m_ambiant   = int(self.m_shared_context.get_data(self.m_columns['ambiant']))

        css3_name = rgb_to_name((
            int(self.m_red * 255 / 1024), \
            int(self.m_green * 255 / 1024), \
            int(self.m_blue * 255 / 1024) \
        ))
        self.m_color = css3_to_spike_colormap[css3_name]

        super().update()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'red' in columns :
            raise Exception('Missing "red" in ' + str(columns) + ' dictionary')
        if not 'green' in columns :
            raise Exception('Missing "green" in ' + str(columns) + ' dictionary')
        if not 'blue' in columns :
            raise Exception('Missing "blue" in ' + str(columns) + ' dictionary')
        if not 'reflected' in columns :
            raise Exception('Missing "reflected" in ' + str(columns) + ' dictionary')
        if not 'ambiant' in columns :
            raise Exception('Missing "ambiant" in ' + str(columns) + ' dictionary')

# pylint: enable=R0902
