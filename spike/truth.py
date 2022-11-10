""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Simulation scenario management
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# system includes
from json import load

# Local includes
from spike.mock import Mock

class Truth(Mock) :
    """ Singleton class describing the robot ground truth """

    m_x_position = 0
    m_y_position = 0
    m_z_position = 0

    m_ports      = {}
    m_structure  = {}

    m_components = {}

    def __new__(cls):

        if not hasattr(cls, 'instance'):
            cls.instance = super(Truth, cls).__new__(cls)
        return cls.instance

    def __init__(self) :
        """ Contructor """

        super().__init__()

        self.s_default_columns  = {
            'x':'x',
            'y':'y',
            'z':'z',
        }

    def load_configuration(self, configuration) :
        """ Loading robot static configuration
        ---
        configuration (str) : Json file containing robots parameters
        """
        conf = {}
        with open(configuration,'r', encoding='UTF-8') as file :
            conf = load(file)
            file.close()

        if 'ports' not in conf :
            raise ValueError('Missing port information in context robot configuration')
        if 'structure' not in conf:
            raise ValueError('Missing structure information in context robot configuration')

        self.m_ports = conf['ports']
        self.m_structure = conf['structure']

    def check_component(self, port, component) :
        """ Check the component type exists on the port
        ---
        port (str)      : port to check
        component (str) : component type to check for
        ---
        returns (bool)  : True if the component exists on the port, False otherwise
        """

        result = False
        if port in self.m_ports :
            if component == self.m_ports[port] :
                result = True
        return result

    def register_component(self, port, component) :
        """ Return type of component hosted by the port
        ---
        port (str)      : port to check
        component (obj) : the component hosted
        """

        if port in self.m_ports :
            test_type = "<class 'spike." + self.m_ports[port].lower() + \
                '.' + self.m_ports[port] + "'>"
            if str(type(component)) == test_type :
                self.m_components[port] = component
            else :
                raise TypeError('component does not fit in port ' + port)
        elif port == 'pair' :
            test_type = "<class 'spike.motorpair.MotorPair'>"
            if str(type(component)) == test_type :
                self.m_components[port] = component
            else :
                raise TypeError('component does not fit in port ' + port)
        elif port == 'hub' :
            test_type = "<class 'spike.hub.PrimeHub'>"
            if str(type(component)) == test_type :
                self.m_components[port] = component
            else :
                raise TypeError('component does not fit in port ' + port)
        else:
            raise TypeError('component does not fit in port ' + port)

    def get_component(self, port) :
        """ Return the component existing on the port
        ---
        port (str)      : port to check
        ---
        returns (obj)   : the component hosted on the port
        """
        result = None
        if port in self.m_components :
            result = self.m_components[port]
        return result

    def step(self) :

        self.m_x_position = int(self.m_scenario['x'][self.m_current_step])
        self.m_y_position = int(self.m_scenario['y'][self.m_current_step])
        self.m_z_position = int(self.m_scenario['z'][self.m_current_step])

        super().step()

    def check_columns(self, columns) :
        """ Check that all the required data have been provided for simulation
        ---
        columns  (dict)   : the excel simulation data associated column name
        """

        if not 'x' in columns :
            raise Exception('Missing "x" in ' + str(columns) + ' dictionary')
        if not 'y' in columns :
            raise Exception('Missing "y" in ' + str(columns) + ' dictionary')
        if not 'z' in columns :
            raise Exception('Missing "z" in ' + str(columns) + ' dictionary')
