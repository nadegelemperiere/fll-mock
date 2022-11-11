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

# pylint: enable=R0801

    def update(self) :
        """ Update the object with current simulation data """

    def check_columns(self, columns) :
        """ Excel content checking function -- to overload
        ---
        columns  (dict)   : The excel simulation data column name
        """


# pylint: enable=R0902
