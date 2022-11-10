# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike motorpair mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------
*** Settings ***
Documentation   A test case to check motorpair mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/truth.json
${EXCEL_DATA_FILE}                ${data}/motor-pair-scenarii.xlsx

*** Test Cases ***

9.1 Ensure MotorPair Is Created With The Required Constants
    [Tags]  MotorPair
    ${scenario}     Create Scenario  ${JSON_CONF_FILE}     ${EXCEL_DATA_FILE}    simple
    ${motor}        Create Object    MotorPair
    @{members} =    Create List      move    start    stop    move_tank    start_tank    start_at_power    start_tank_at_power    get_default_speed    set_motor_rotation    set_default_speed    set_stop_action
    Should Have Members    ${motor}    ${members}

9.2 Ensure Error Management Is Correctly Implemented
    [Tags]  MotorPair
    ${scenario}     Create Scenario  ${JSON_CONF_FILE}     ${EXCEL_DATA_FILE}    simple
    ${motor}        Create Object    MotorPair
    Run Keyword And Expect Error     TypeError: amount is not a number                    Use Object Method  ${motor}     move                   False    -1    whatever    cm    0    100
    Run Keyword And Expect Error     TypeError: unit is not a string                      Use Object Method  ${motor}     move                   False    -1    180    100    0     100
    Run Keyword And Expect Error     ValueError: unit is not one of the allowed values    Use Object Method  ${motor}     move                   False    -1    180    whatever    0    100
    Run Keyword And Expect Error     TypeError: steering is not an integer                Use Object Method  ${motor}     move                   False    -1    100    cm    100.0  100
    Run Keyword And Expect Error     TypeError: speed is not an integer                   Use Object Method  ${motor}     move                   False    -1    100    cm    100    100.0
    Run Keyword And Expect Error     TypeError: steering is not an integer                Use Object Method  ${motor}     start                  False    -1    100.0  100
    Run Keyword And Expect Error     TypeError: speed is not an integer                   Use Object Method  ${motor}     start                  False    -1    100    100.0
    Run Keyword And Expect Error     TypeError: amount is not a number                    Use Object Method  ${motor}     move_tank              False    -1    whatever    cm    0    100
    Run Keyword And Expect Error     TypeError: unit is not a string                      Use Object Method  ${motor}     move_tank              False    -1    180    100    0     100
    Run Keyword And Expect Error     ValueError: unit is not one of the allowed values    Use Object Method  ${motor}     move_tank              False    -1    180    whatever    0    100
    Run Keyword And Expect Error     TypeError: left_speed is not an integer              Use Object Method  ${motor}     move_tank              False    -1    100    cm    100.0  100
    Run Keyword And Expect Error     TypeError: right_speed is not an integer             Use Object Method  ${motor}     move_tank              False    -1    100    cm    100    100.0
    Run Keyword And Expect Error     TypeError: left_speed is not an integer              Use Object Method  ${motor}     start_tank             False    -1    100.0  100
    Run Keyword And Expect Error     TypeError: right_speed is not an integer             Use Object Method  ${motor}     start_tank             False    -1    100    100.0
    Run Keyword And Expect Error     TypeError: power is not an integer                   Use Object Method  ${motor}     start_at_power         False    -1    100.0  100
    Run Keyword And Expect Error     TypeError: steering is not an integer                Use Object Method  ${motor}     start_at_power         False    -1    100    100.0
    Run Keyword And Expect Error     TypeError: left_power is not an integer              Use Object Method  ${motor}     start_tank_at_power    False    -1    100.0  100
    Run Keyword And Expect Error     TypeError: right_power is not an integer             Use Object Method  ${motor}     start_tank_at_power    False    -1    100    100.0
    Run Keyword And Expect Error     TypeError: amount is not a number                    Use Object Method  ${motor}     set_motor_rotation     False    -1    whatever    cm
    Run Keyword And Expect Error     TypeError: unit is not a string                      Use Object Method  ${motor}     set_motor_rotation     False    -1    180    100
    Run Keyword And Expect Error     ValueError: unit is not one of the allowed values    Use Object Method  ${motor}     set_motor_rotation     False    -1    180    whatever
    Run Keyword And Expect Error     TypeError: speed is not a number                     Use Object Method  ${motor}     set_default_speed      False    -1    100.0
    Run Keyword And Expect Error     TypeError: action is not a string                    Use Object Method  ${motor}     set_stop_action        False    -1    95.5
    Run Keyword And Expect Error     ValueError: action is not one of the allowed values  Use Object Method  ${motor}     set_stop_action        False    -1    whatever
