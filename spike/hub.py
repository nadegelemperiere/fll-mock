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

    m_shared_truth  = None

    def __init__(self) :
        """ Contructor """

        self.left_button    = Button()
        self.right_button   = Button()
        self.speaker        = Speaker()
        self.light_matrix   = LightMatrix()
        self.status_light   = StatusLight
        self.motion_sensor  = MotionSensor()

        self.m_shared_truth = Truth()
        self.m_shared_truth.register_component('hub', self)
