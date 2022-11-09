""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Generic mission code
# -------------------------------------------------------
# Each mission differ, but at some points requires to go there,
# and then move back
# -------------------------------------------------------
# Nadège LEMPERIERE, @19 october 2022
# Latest revision: 19 october 2022
# --------------------------------------------------- """

# Local includes
from spike.button       import Button
from spike.speaker      import Speaker
from spike.lightmatrix  import LightMatrix
from spike.statuslight  import StatusLight
from spike.motionsensor import MotionSensor

# Constants
hub_ports = ['A', 'B', 'C', 'D', 'E', 'F']

class PrimeHub() :
    """ Hub mocking function """

    left_button     = None
    right_button    = None
    speaker         = None
    light_matrix    = None
    status_light    = None
    motion_sensor   = None

    m_ports         = {}

    def __init__(self) :
        """ Contructor """

        self.left_button    = Button()
        self.right_button   = Button()
        self.speaker        = Speaker()
        self.light_matrix   = LightMatrix()
        self.status_light   = StatusLight
        self.motion_sensor  = MotionSensor()

# ----------------- SIMULATION FUNCTIONS -----------------

    def connect(self, ports) :
        """ Sets the elements connected to the hub
        ---
        ports (dict) : Mapping between port and element types
        """

        self.m_ports = {}
        for key,val in ports.items() :
            if key not in hub_ports :
                raise ValueError('port ' + key + ' not one of allowed ports')
            self.m_ports[key] = val
