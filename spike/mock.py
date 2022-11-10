""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Generic mock class containing shared functions
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# Local include
from spike.context import Context

class Mock() :
    """ Generic mock class """

    m_scenario          = {}
    m_commands          = {}
    m_current_step      = -1
    m_columns           = {}
    m_shared_context    = None
    m_shared_truth      = None

    s_default_columns   = {}

# ------------ SPIKE GENERIC MOCK FUNCTIONS --------------

    def __init__(self) :
        """ Contructor
        ---
        columns  (dict)   : The excel simulation data column name
        """
        self.m_scenario         = {}
        self.m_commands         = {}
        self.m_current_step     = -1
        self.m_columns          = {}
        self.m_shared_context   = Context()
        self.m_shared_truth     = None

# ----------------- SIMULATION FUNCTIONS -----------------

    def columns(self, columns = None) :
        """ Define the mapping between excel file columns and
            the mock requied data
        ---
        columns  (dict) : The excel simulation data column name
        """
        if columns is None : columns = self.s_default_columns
        self.check_columns(columns)
        self.m_columns = columns

# pylint: disable=R0801
    def initialize(self) :
        """ Initialize simulation from context """
        if len(self.m_columns) == 0 :
            self.m_columns = self.s_default_columns

        self.m_scenario = {}
        data = self.m_shared_context.get_data()
        for column in self.m_columns :
            if self.m_columns[column] not in data :
                col = self.m_columns[column]
                message = str(type(self)) + ' : "' + col + '" data not found in excel sheet'
                raise Exception(message)
            self.m_scenario[column] = []
            for value in data[self.m_columns[column]]:
                self.m_scenario[column].append(value)

        self.restart()
# pylint: enable=R0801

    def restart(self) :
        """ Restart simulation """
        self.m_current_step = 0

    def step(self) :
        """ Step to the next simulation step -- to overload """
        self.m_current_step += 1

    def check_columns(self, columns) :
        """ Excel content checking function -- to overload
        ---
        columns  (dict)   : The excel simulation data column name
        """

    def get_commands(self) :
        """ Commands received by mock
        ---
        returns  (dict)   : A dict of list of command values
        """
        return self.m_commands


# pylint: enable=R0902
