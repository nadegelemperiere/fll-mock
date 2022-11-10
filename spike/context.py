""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Simulation scenario management
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# Openpyxl includes
from openpyxl import load_workbook

class Context() :
    """ Singleton class managing a simulation context """

    m_data          = {}

    def __new__(cls):

        if not hasattr(cls, 'instance'):
            cls.instance = super(Context, cls).__new__(cls)
        return cls.instance

    def load(self, filename, sheet) :
        """ Read scenario from excel file
        ---
        filename (str)  : Excel file in which the scenario data are located
        sheet (str)     : Sheet from which data shall be retrieved
        """

        self.m_data = {}

        # Load workbook with value rather than formula
        wbook = load_workbook(filename, data_only = True)

        # Select sheet
        content_sheet = wbook[sheet]

        # Associate header to column
        i_column = 1
        column_to_header = {}
        header_to_column = {}
        content = content_sheet.cell(1,i_column).value
        while content is not None :
            column_to_header[i_column]  = content
            header_to_column[content]   = i_column
            self.m_data[content] = []
            i_column += 1
            content = content_sheet.cell(1,i_column).value
        if 'time' not in header_to_column : raise Exception('Time column not found')

        for i_row in range(2,content_sheet.max_row + 1) :
            for col,header in column_to_header.items() :
                value = content_sheet.cell(i_row,col).value
                if isinstance(value,str) and value == 'True'  : value = True
                if isinstance(value,str) and value == 'False' : value = False
                self.m_data[header].append(value)

    def get_data(self) :
        """ Return scenario data
        ---
        returns (dict)  : Scenario data
        """
        return self.m_data
