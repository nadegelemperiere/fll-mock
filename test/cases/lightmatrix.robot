# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike light matrix mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check light matrix mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/truth.json
${EXCEL_DATA_FILE}                ${data}/light-matrix-scenarii.xlsx

*** Test Cases ***

6.1 Ensure Light Matrix Is Created With The Required Constants
    [Tags]  LightMatrix
    Create Scenario     ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${matrix}       Create Object    LightMatrix
    @{members} =    Create List      show_image    set_pixel    write     off
    Should Have Members    ${matrix}    ${members}

6.2 Test Light Matrix Image Display
    [Tags]    LightMatrix
    Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${matrix}          Create Object      LightMatrix
    Use Object Method  ${matrix}          initialize
    Play Scenario During Steps  ${matrix}     1
    Use Object Method  ${matrix}  show_image    False    -1    HEART
    ${heart}       Use Object Method  ${matrix}   get_matrix    True
    ${p}           Get From List      ${heart}    0
    Should Be Equal As Integers   ${p}        0
    ${p}           Get From List      ${heart}    1
    Should Be Equal As Integers   ${p}        100
    Use Object Method  ${matrix}  set_pixel   False    -1    0    0    50
    ${heart}       Use Object Method  ${matrix}   get_matrix    True
    ${p}           Get From List      ${heart}    0
    Should Be Equal As Integers   ${p}        50
    Use Object Method  ${matrix}  off
    ${empty}       Use Object Method  ${matrix}   get_matrix    True
    ${p}           Get From List      ${empty}    0
    Should Be Equal As Integers   ${p}        0
    ${p}           Get From List      ${empty}    1
    Should Be Equal As Integers   ${p}        0
