# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike hub button mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check hub button mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/configuration.json
${EXCEL_DATA_FILE}                ${data}/button-scenarii.xlsx

*** Test Cases ***

1.1 Ensure Button Is Created With The Required Constants
    [Tags]              Button
    ${scenario}         Create Scenario  ${JSON_CONF_FILE}
    ${button}           Create Object    Button
    @{members} =        Create List    wait_until_pressed    wait_until_released    was_pressed    is_pressed
    Should Have Members    ${button}    ${members}

1.2 Test Button Behavior On Simple Scenario
    [Tags]              Button
    ${scenario}         Create Scenario        ${JSON_CONF_FILE}
    ${button}           Create Object          Button
    ${scenario}         Initialize Scenario    ${scenario}   ${EXCEL_DATA_FILE}    simple    ${button}
    @{steps} =          Create List    36    20    2    46
    @{is_pressed} =     Create List
    @{was_pressed} =    Create List
    FOR    ${step}    IN    @{steps}
        Play Scenario During Steps  ${button}     ${step}
        ${is_p}         Use Object Method  ${button}    is_pressed    True
        ${was_p}        Use Object Method  ${button}    was_pressed    True
        Append To List  ${is_pressed}    ${is_p}
        Append To List  ${was_pressed}    ${was_p}
    END
    Should Be True      ${is_pressed[0]}
    Should Be True      ${was_pressed[0]}
    Should Not Be True  ${is_pressed[1]}
    Should Be True      ${was_pressed[1]}
    Should Not Be True  ${is_pressed[2]}
    Should Not Be True  ${was_pressed[2]}
    Should Be True      ${is_pressed[3]}
    Should Be True      ${was_pressed[3]}

1.3 Test The Parallel Behaviour Of Wait functions
    [Tags]              Button
    ${scenario}         Create Scenario        ${JSON_CONF_FILE}
    ${button}           Create Object          Button
    ${scenario}         Initialize Scenario    ${scenario}   ${EXCEL_DATA_FILE}    simple    ${button}
    ${thread}           Start Method In A Thread    ${button}    wait_until_pressed
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${button}     36
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
    ${thread}           Start Method In A Thread    ${button}    wait_until_released
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${button}     20
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
