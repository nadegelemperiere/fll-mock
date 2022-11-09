# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike hub speaker mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check hub speaker mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/configuration.json
${EXCEL_DATA_FILE}                ${data}/speaker-scenarii.xlsx

*** Test Cases ***

10.1 Ensure Speaker Is Created With The Required Constants
    [Tags]  Speaker
    ${scenario}         Create Scenario  ${JSON_CONF_FILE}
    ${speaker}          Create Object    Speaker
    @{members} =        Create List    beep    start_beep    stop    get_volume    set_volume
    Should Have Members    ${speaker}    ${members}

10.2 Test Speaker Behavior
    [Tags]  Speaker
    ${scenario}         Create Scenario      ${JSON_CONF_FILE}
    ${speaker}          Create Object        Speaker
    ${scenario}         Initialize Scenario  ${scenario}    ${EXCEL_DATA_FILE}    simple    ${speaker}
    Use Object Method  ${speaker}    set_volume    False    -1    50
    ${volume}            Use Object Method  ${speaker}    get_volume    True
    Should Be Equal As Numbers    ${volume}    50

10.3 Test The Parallel Behaviour Of Beep functions
    [Tags]  Speaker
    ${scenario}         Create Scenario      ${JSON_CONF_FILE}
    ${speaker}          Create Object        Speaker
    ${scenario}         Initialize Scenario  ${scenario}    ${EXCEL_DATA_FILE}    simple    ${speaker}
    Play Scenario During Steps  ${speaker}     0
    ${thread}           Start Method In A Thread    ${speaker}    beep    60    2
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${speaker}     10
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${speaker}     15
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}