# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike hub status light mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check hub status light mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/truth.json
${EXCEL_DATA_FILE}                ${data}/status-light-scenarii.xlsx

*** Test Cases ***

11.1 Ensure Status Light Is Created With The Required Constants
    [Tags]    StatusLight
    Create Scenario  ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${light}         Create Object      StatusLight
    @{members} =     Create List        on    off
    Should Have Members    ${light}    ${members}

11.2 Ensure Error Management Is Correctly Implemented
    [Tags]    StatusLight
    Create Scenario  ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${light}         Create Object      StatusLight
    Run Keyword And Expect Error    TypeError: color is not a string                    Use Object Method  ${light}     on    False    -1    100.0
    Run Keyword And Expect Error    ValueError: color is not one of the allowed values  Use Object Method  ${light}     on    False    -1    whatever

11.3 Test Status Light Behavior
    [Tags]    StatusLight
    Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${light}           Create Object      StatusLight
    Play Scenario During Steps  ${light}     1
    Use Object Method  ${light}    on    False    -1    red
    ${color}           Use Object Method  ${light}    get_color    True
    ${status}          Use Object Method  ${light}    get_status    True
    Should Be Equal    ${color}     red
    Should Be Equal    ${status}    True
    Use Object Method  ${light}    off   False    -1
    ${color}           Use Object Method  ${light}    get_color    True
    ${status}          Use Object Method  ${light}    get_status    True
    Should Be Equal    ${color}     red
    Should Be Equal    ${status}    False