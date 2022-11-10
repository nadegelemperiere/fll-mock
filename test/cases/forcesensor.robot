# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike force sensor mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check force sensor mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/truth.json
${EXCEL_DATA_FILE}                ${data}/force-sensor-scenarii.xlsx

*** Test Cases ***

4.1 Ensure Force Sensor Is Created With The Required Constants
    [Tags]    ForceSensor
    Create Scenario  ${JSON_CONF_FILE}    ${EXCEL_DATA_FILE}    simple
    ${sensor}        Create Object    ForceSensor
    @{members} =     Create List    wait_until_pressed    wait_until_released    is_pressed    get_force_newton    get_force_percentage
    Should Have Members    ${sensor}    ${members}

4.2 Test Force Sensor Behavior On Simple Scenario
    [Tags]    ForceSensor
    Create Scenario         ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${sensor}               Create Object      ForceSensor
    Use Object Method       ${sensor}          initialize
    @{steps} =              Create List    20    9      11    10    20
    @{is_pressed} =         Create List
    @{force} =              Create List    0     1.2    7     9.2    0
    @{force_percentage} =   Create List    0     12     70    92     0
    ${i_step} =         Set Variable    0
    ${i_step} =         Convert To Integer  ${i_step}
    FOR    ${step}    IN    @{steps}
        Play Scenario During Steps  ${sensor}     ${step}
        ${is_p}         Use Object Method  ${sensor}    is_pressed    True
        ${f}        Use Object Method  ${sensor}    get_force_newton        True    -1
        ${p}        Use Object Method  ${sensor}    get_force_percentage    True    -1
        Append To List  ${is_pressed}    ${is_p}
        ${ft}       Get From List      ${force}              ${i_step}
        ${pt}       Get From List      ${force_percentage}   ${i_step}
        Should Be Equal As Numbers     ${ft}     ${f}
        Should Be Equal As Integers    ${pt}     ${p}
        ${i_step} =     Set Variable   ${i_step + 1}
    END
    Should Not Be True  ${is_pressed[0]}
    Should Not Be True  ${is_pressed[1]}
    Should Be True      ${is_pressed[2]}
    Should Be True      ${is_pressed[3]}
    Should Not Be True  ${is_pressed[4]}

4.3 Test The Parallel Behaviour Of Wait functions
    [Tags]    ForceSensor
    Create Scenario     ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${sensor}           Create Object      ForceSensor
    Use Object Method   ${sensor}          initialize
    ${thread}           Start Method In A Thread    ${sensor}    wait_until_pressed
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     35
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
    ${thread}           Start Method In A Thread    ${sensor}    wait_until_released
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     25
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
