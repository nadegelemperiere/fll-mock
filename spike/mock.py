""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Generic mock class containing shared functions
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

class Mock() :
    """ Generic mock class """

    m_scenario          = {}
    m_current_step      = -1
    m_columns           = {}

    s_default_columns   = {}

# ------------ SPIKE GENERIC MOCK FUNCTIONS --------------

    def __init__(self) :
        """ Contructor
        ---
        columns  (dict)   : The excel simulation data column name
        """
        self.m_scenario         = {}
        self.m_current_step     = -1

# ----------------- SIMULATION FUNCTIONS -----------------

    def configure(self, columns = None) :
        """ Define the mapping between excel file columns and
            the mock requied data
        ---
        columns  (dict) : The excel simulation data column name
        """
        if columns is None : columns = self.s_default_columns
        self.check_columns(columns)
        self.m_columns = columns

# pylint: disable=R0801
    def initialize(self, data) :
        """ Initialize simulation from scenario data
        ---
        data (dict)     : Simulation data
        """
        if len(self.m_columns) == 0 :
            self.m_columns = self.s_default_columns

        self.m_scenario = {}
        for column in self.m_columns :
            if self.m_columns[column] not in data :
                col = self.m_columns[column]
                message = str(type(self)) + ' : "' + col + '" data not found in excel sheet'
                raise Exception(message)
            self.m_scenario[column] = []
            for status in data[self.m_columns[column]]:
                self.m_scenario[column].append(status)

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

# pylint: enable=R0902
