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

# Openpyxl includes
from openpyxl import load_workbook

# Local includes
from spike.mock import Mock

class Truth(Mock) :
    """ Class describing the robot ground truth """

    m_x_position = 0
    m_y_position = 0
    m_z_position = 0

    m_ports      = {}
    m_structure  = {}

    m_components = {}

    def __init__(self) :
        """ Contructor """

        self.m_ports      = {}
        self.m_structure  = {}

        self.s_default_columns  = {
            'x':'x',
            'y':'y',
            'z':'z',
        }

    def configure(self, configuration) :
        """ Configure real robot context
        ---
        configuration  (dict)   : the robot static configuration
        """
        if not 'ports' in configuration :
            raise ValueError('Missing port information in context robot configuration')
        if not 'structure' in configuration :
            raise ValueError('Missing structure information in context robot configuration')

        self.m_ports = configuration['ports']
        self.m_structure = configuration['structure']

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
