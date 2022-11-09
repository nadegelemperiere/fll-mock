# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike distance sensor mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check distance sensor mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/configuration.json
${EXCEL_DATA_FILE}                ${data}/distance-sensor-scenarii.xlsx

*** Test Cases ***

3.1 Ensure Distance Sensor Is Created With The Required Constants
    [Tags]    DistanceSensor
    ${scenario}     Create Scenario  ${JSON_CONF_FILE}
    ${sensor}       Create Object    DistanceSensor
    @{members} =    Create List    get_distance_cm    get_distance_inches    get_distance_percentage    wait_for_distance_farther_than    wait_for_distance_closer_than     light_up     light_up_all
    Should Have Members    ${sensor}    ${members}

3.2 Ensure Error Management Is Correctly Implemented
    [Tags]    DistanceSensor
    ${scenario}         Create Scenario  ${JSON_CONF_FILE}
    ${sensor}           Create Object    DistanceSensor
    Run Keyword And Expect Error    TypeError: brightness is not an integer     Use Object Method  ${sensor}     light_up_all    False    -1    12.5
    Run Keyword And Expect Error    TypeError: right_top is not an integer      Use Object Method  ${sensor}     light_up        False    -1    12.5  50    50    50
    Run Keyword And Expect Error    TypeError: left_top is not an integer       Use Object Method  ${sensor}     light_up        False    -1    50    12.5  50    50
    Run Keyword And Expect Error    TypeError: right_bottom is not an integer   Use Object Method  ${sensor}     light_up        False    -1    50    50    12.5  50
    Run Keyword And Expect Error    TypeError: left_bottom is not an integer    Use Object Method  ${sensor}     light_up        False    -1    50    50    50    12.5

3.3 Test Distance Sensor Behavior On Simple Scenario
    [Tags]    DistanceSensor
    ${scenario}                    Create Scenario      ${JSON_CONF_FILE}
    ${sensor}                      Create Object        DistanceSensor
    ${scenario}                    Initialize Scenario  ${scenario}    ${EXCEL_DATA_FILE}    simple    ${sensor}
    @{steps} =                     Create List    4      20     10     15     25
    @{distance_cm_lr} =            Create List    -1     70     40     160    -1
    @{distance_inches_lr} =        Create List    -1     28     16     63     -1
    @{distance_percentage_lr} =    Create List    -1     35     20     80     -1
    @{distance_cm_sr} =            Create List    -1     -1     40     -1     -1
    @{distance_inches_sr} =        Create List    -1     -1     16     -1     -1
    @{distance_percentage_sr} =    Create List    -1     -1     20     -1     -1
    ${i_step} =         Set Variable    0
    ${i_step} =         Convert To Integer  ${i_step}
    FOR    ${step}    IN    @{steps}
        Play Scenario During Steps     ${sensor}    ${step}
        ${c}        Use Object Method  ${sensor}    get_distance_cm            True    -1
        ${i}        Use Object Method  ${sensor}    get_distance_inches        True    -1
        ${p}        Use Object Method  ${sensor}    get_distance_percentage    True    -1
        ${ct}       Get From List      ${distance_cm_lr}           ${i_step}
        ${it}       Get From List      ${distance_inches_lr}       ${i_step}
        ${pt}       Get From List      ${distance_percentage_lr}   ${i_step}
        Should Be Equal As Integers    ${ct}     ${c}
        Should Be Equal As Integers    ${it}     ${i}
        Should Be Equal As Integers    ${pt}     ${p}
        ${c}        Use Object Method  ${sensor}    get_distance_cm            True    -1    True
        ${i}        Use Object Method  ${sensor}    get_distance_inches        True    -1    True
        ${p}        Use Object Method  ${sensor}    get_distance_percentage    True    -1    True
        ${ct}       Get From List      ${distance_cm_sr}           ${i_step}
        ${it}       Get From List      ${distance_inches_sr}       ${i_step}
        ${pt}       Get From List      ${distance_percentage_sr}   ${i_step}
        Should Be Equal As Integers    ${ct}     ${c}
        Should Be Equal As Integers    ${it}     ${i}
        Should Be Equal As Integers    ${pt}     ${p}
        ${i_step} =     Set Variable   ${i_step + 1}
    END

3.4 Test The Parallel Behaviour Of Wait functions
    [Tags]              DistanceSensor
    ${scenario}         Create Scenario      ${JSON_CONF_FILE}
    ${sensor}           Create Object        DistanceSensor
    ${scenario}         Initialize Scenario  ${scenario}    ${EXCEL_DATA_FILE}    simple    ${sensor}
    Play Scenario During Steps  ${sensor}     10
    ${thread}           Start Method In A Thread    ${sensor}    wait_for_distance_closer_than    170    cm    False
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     20
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
    ${thread}           Start Method In A Thread    ${sensor}    wait_for_distance_farther_than    160    cm    False
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     60
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
    ${thread}           Start Method In A Thread    ${sensor}    wait_for_distance_closer_than     30    cm    True
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     50
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
    ${thread}           Start Method In A Thread    ${sensor}    wait_for_distance_farther_than    40    cm    True
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     45
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
