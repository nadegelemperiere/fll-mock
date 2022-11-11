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
from spike.truth        import Truth
from spike.mock         import Mock

# Constants
hub_ports = ['A', 'B', 'C', 'D', 'E', 'F']

# pylint: disable=R0902
class PrimeHub(Mock) :
    """ Hub mocking function """

    left_button     = None
    right_button    = None
    speaker         = None
    light_matrix    = None
    status_light    = None
    motion_sensor   = None

    m_shared_truth  = None

    def __init__(self) :
        """ Contructor """
        super().__init__()

        self.left_button    = Button()
        self.right_button   = Button()
        self.speaker        = Speaker()
        self.light_matrix   = LightMatrix()
        self.status_light   = StatusLight()
        self.motion_sensor  = MotionSensor()

        self.s_default_columns  = {
            'time'              : 'time',
            'is_left_pressed'   : 'is_left_pressed',
            'is_right_pressed'  : 'is_right_pressed',
            'yaw'               : 'yaw',
            'pitch'             : 'pitch',
            'roll'              : 'roll',
            'gesture'           : 'gesture',
        }
        self.left_button.columns({
            'time'       : 'time',
            'is_pressed' : 'is_left_pressed'
        })
        self.right_button.columns({
            'time'       : 'time',
            'is_pressed' : 'is_right_pressed'
        })

        self.m_shared_truth = Truth()
        self.m_shared_truth.register_component('hub', self)

# ----------------- SIMULATION FUNCTIONS -----------------

    def columns(self, columns = None) :
        """ Define the mapping between excel file columns and
            the mock requied data
        ---
        columns  (dict) : The excel simulation data column name
        """
        self.left_button.columns({
            'time'       : self.m_columns['time'],
            'is_pressed' : self.m_columns['is_left_pressed'],
        })
        self.right_button.columns({
            'time'       : self.m_columns['time'],
            'is_pressed' : self.m_columns['is_right_pressed'],
        })
        self.speaker.columns({
            'time'       : self.m_columns['time'],
        })
        self.light_matrix.columns({
            'time'       : self.m_columns['time'],
        })
        self.status_light.columns({
            'time'       : self.m_columns['time'],
        })
        self.motion_sensor.columns({
            'time'       : self.m_columns['time'],
            'yaw'        : self.m_columns['yaw'],
            'pitch'      : self.m_columns['pitch'],
            'roll'       : self.m_columns['roll'],
            'gesture'    : self.m_columns['gesture'],
        })

    def update(self) :
        """ Step to the next simulation step """

        self.left_button.update()
        self.right_button.update()
        self.speaker.update()
        self.light_matrix.update()
        self.status_light.update()
        self.motion_sensor.update()
