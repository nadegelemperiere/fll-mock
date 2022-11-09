# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike timer mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check timer functioning
Library         ../keywords/objects.py
Library         Collections


*** Variables ***
${JSON_CONF_FILE}                 ${data}/configuration.json
${EXCEL_DATA_FILE}                ${data}/timer-scenarii.xlsx

*** Test Cases ***
12.1 Ensure Timer Is Created With The Required Constants
    [Tags]  Timer
    ${scenario}      Create Scenario      ${JSON_CONF_FILE}
    ${timer}         Create Object    Timer
    @{members} =     Create List    now    reset
    Should Have Members    ${timer}    ${members}

12.2 Test Timer Behavior
    [Tags]  Timer
    ${scenario}         Create Scenario      ${JSON_CONF_FILE}
    ${s_timer}          Create Object        TimerSingleton
    ${scenario}         Initialize Scenario  ${scenario}    ${EXCEL_DATA_FILE}    simple    ${s_timer}
    Play Scenario During Steps  ${s_timer}     10
    ${timer1}           Create Object    Timer
    Use Object Method  ${timer1}    reset    False
    Play Scenario During Steps  ${s_timer}     20
    ${delay}            Use Object Method  ${timer1}    now    True
    Should Be Equal As Numbers    ${delay}    2
    ${timer2}            Create Object    Timer
    Use Object Method  ${timer2}    reset    False
    Play Scenario During Steps  ${s_timer}     1
    ${delay}            Use Object Method  ${timer2}    now    True
    Should Be Equal As Numbers    ${delay}    0.1

12.3 Test The Parallel Behaviour Of Wait functions
    [Tags]  Timer
    ${scenario}         Create Scenario      ${JSON_CONF_FILE}
    ${s_timer}          Create Object        TimerSingleton
    ${scenario}         Initialize Scenario  ${scenario}    ${EXCEL_DATA_FILE}    simple    ${s_timer}
    Play Scenario During Steps  ${s_timer}     1
    ${thread}           Start Function In A Thread    wait_for_seconds    2
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${s_timer}     10
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${s_timer}     20
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}

