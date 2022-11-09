# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike hub mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check hub mock functioning
Library         ../keywords/objects.py

*** Test Cases ***

5.1 Ensure Hub Is Created With The Required Constants
    [Tags]    Hub
    ${hub}          Create Object    Hub
    @{members} =    Create List    left_button    right_button    speaker    light_matrix    status_light    motion_sensor
    Should Have Members    ${hub}    ${members}