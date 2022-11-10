# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike color sensor mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check color sensor mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/truth.json
${EXCEL_DATA_FILE}                ${data}/color-sensor-scenarii.xlsx

*** Test Cases ***

2.1 Ensure Color Sensor Is Created With The Required Constants
    [Tags]    ColorSensor
    Create Scenario  ${JSON_CONF_FILE}    ${EXCEL_DATA_FILE}    simple
    ${sensor}        Create Object    ColorSensor
    @{members} =     Create List    get_color    get_ambiant_light    get_reflected_light    get_rgb_intensity    get_red     get_green     get_blue     wait_until_color    wait_for_new_color     light_up     light_up_all
    Should Have Members    ${sensor}    ${members}

2.2 Ensure Error Management Is Correctly Implemented
    [Tags]  ColorSensor
    Create Scenario  ${JSON_CONF_FILE}    ${EXCEL_DATA_FILE}    simple
    ${sensor}        Create Object    ColorSensor
    Run Keyword And Expect Error    TypeError: brightness is not an integer    Use Object Method  ${sensor}     light_up_all    False    -1    12.5
    Run Keyword And Expect Error    TypeError: light_1 is not an integer       Use Object Method  ${sensor}     light_up        False    -1    12.5  50    50
    Run Keyword And Expect Error    TypeError: light_2 is not an integer       Use Object Method  ${sensor}     light_up        False    -1    50    12.5    50
    Run Keyword And Expect Error    TypeError: light_3 is not an integer       Use Object Method  ${sensor}     light_up        False    -1    50    50    12.5

2.3 Test Color Sensor Behavior On Simple Scenario
    [Tags]  ColorSensor
    Create Scenario     ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${sensor}           Create Object      ColorSensor
    Use Object Method   ${sensor}          initialize
    @{steps} =          Create List    40      20       30      50       50
    @{red} =            Create List    1024    0        1024    0        0
    @{blue} =           Create List    1024    0        0       0        1024
    @{green} =          Create List    1024    0        0       1024     0
    @{color} =          Create List    white   black    red     green    blue
    @{ambiant} =        Create List    0       0        0       0        0
    @{reflected} =      Create List    100     100      100     100      100
    ${i_step} =         Set Variable    0
    ${i_step} =         Convert To Integer  ${i_step}
    FOR    ${step}    IN    @{steps}
        Play Scenario During Steps     ${sensor}    ${step}
        ${r}        Use Object Method  ${sensor}    get_red                True
        ${g}        Use Object Method  ${sensor}    get_green              True
        ${b}        Use Object Method  ${sensor}    get_blue               True
        ${c}        Use Object Method  ${sensor}    get_color              True
        ${a}        Use Object Method  ${sensor}    get_ambiant_light      True
        ${rf}       Use Object Method  ${sensor}    get_reflected_light    True
        ${i}        Use Object Method  ${sensor}    get_rgb_intensity      True
        ${rt}       Get From List      ${red}          ${i_step}
        ${gt}       Get From List      ${green}        ${i_step}
        ${bt}       Get From List      ${blue}         ${i_step}
        ${ct}       Get From List      ${color}        ${i_step}
        ${at}       Get From List      ${ambiant}      ${i_step}
        ${rft}      Get From List      ${reflected}    ${i_step}
        Should Be Equal As Integers    ${rt}     ${r}
        Should Be Equal As Integers    ${gt}     ${g}
        Should Be Equal As Integers    ${bt}     ${b}
        Should Be Equal                ${ct}     ${c}
        Should Be Equal As Integers    ${at}     ${a}
        Should Be Equal As Integers    ${rft}    ${rf}
        ${i_step} =     Set Variable   ${i_step + 1}
    END

2.4 Test The Parallel Behaviour Of Wait functions
    [Tags]  ColorSensor
    Create Scenario     ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${sensor}           Create Object      ColorSensor
    Use Object Method   ${sensor}          initialize
    Play Scenario During Steps  ${sensor}     10
    ${thread}           Start Method In A Thread    ${sensor}    wait_until_color    red
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     50
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     30
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
    ${c}        Use Object Method  ${sensor}    wait_for_new_color  True
    Should Be Equal     red    ${c}
    ${thread}           Start Method In A Thread    ${sensor}    wait_for_new_color
    ${is_alive}         Is Thread Running    ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}     50
    ${is_alive}         Is Thread Running    ${thread}
    Should Not Be True  ${is_alive}
    ${c}        Use Object Method  ${sensor}    get_color  True
    Should Be Equal     green    ${c}

2.5 Test The Light Adjustment Functions And Their Impact On Color
    [Tags]  ColorSensor
    Create Scenario    ${JSON_CONF_FILE}    ${EXCEL_DATA_FILE}    simple
    ${sensor}          Create Object      ColorSensor
    Use Object Method  ${sensor}           initialize
    Play Scenario During Steps  ${sensor}     1
    ${c}                Use Object Method  ${sensor}    get_color  True
    Should Be Equal     white    ${c}
    Use Object Method  ${sensor}    light_up_all  False    -1    0
    Play Scenario During Steps  ${sensor}     1
    ${c}                Use Object Method  ${sensor}    get_color  True
    Should Be Equal     black    ${c}
    Play Scenario During Steps  ${sensor}     2
    ${c}                Use Object Method  ${sensor}    get_color  True
    Should Be Equal     black    ${c}
    Use Object Method  ${sensor}    light_up  False    -1    100    100    100
    Play Scenario During Steps  ${sensor}     1
    ${c}                Use Object Method  ${sensor}    get_color  True
    Should Be Equal     white    ${c}


