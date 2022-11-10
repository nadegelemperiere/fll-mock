# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike motor mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check motor mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/truth.json
${EXCEL_DATA_FILE}                ${data}/motor-scenarii.xlsx

*** Test Cases ***

8.1 Ensure Motor Is Created With The Required Constants
    [Tags]  Motor
    Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${motor}           Create Object      Motor
    @{members} =       Create List        run_to_position    run_to_degrees_counted    run_for_degrees    run_for_rotations    run_for_seconds    start    stop    start_at_power    get_speed    get_position    get_degrees_counted    get_default_speed    was_interrupted    was_stalled    set_degrees_counted    set_default_speed    set_stop_action    set_stall_detection
    Should Have Members    ${motor}    ${members}

8.2 Ensure Error Management Is Correctly Implemented
    [Tags]    Motor
    Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${motor}           Create Object      Motor
    Run Keyword And Expect Error    TypeError: degrees is not an integer                       Use Object Method  ${motor}     run_to_position         False    -1    180.5     shortest path    100
    Run Keyword And Expect Error    TypeError: direction is not a string                       Use Object Method  ${motor}     run_to_position         False    -1    180       100              100
    Run Keyword And Expect Error    TypeError: speed is not an integer                         Use Object Method  ${motor}     run_to_position         False    -1    180       shortest path    95.5
    Run Keyword And Expect Error    ValueError: direction is not one of the allowed values     Use Object Method  ${motor}     run_to_position         False    -1    180       whatever         100
    Run Keyword And Expect Error    ValueError: degrees is not in the range 0-359              Use Object Method  ${motor}     run_to_position         False    -1    360       shortest path    100
    Run Keyword And Expect Error    ValueError: degrees is not in the range 0-359              Use Object Method  ${motor}     run_to_position         False    -1    -1        shortest path    100
    Run Keyword And Expect Error    TypeError: degrees is not an integer                       Use Object Method  ${motor}     run_to_degrees_counted  False    -1    95.5      100
    Run Keyword And Expect Error    TypeError: speed is not an integer                         Use Object Method  ${motor}     run_to_degrees_counted  False    -1    180       95.5
    Run Keyword And Expect Error    TypeError: degrees is not an integer                       Use Object Method  ${motor}     run_for_degrees         False    -1    95.5      100
    Run Keyword And Expect Error    TypeError: speed is not an integer                         Use Object Method  ${motor}     run_for_degrees         False    -1    180       95.5
    Run Keyword And Expect Error    TypeError: rotations is not a number                       Use Object Method  ${motor}     run_for_rotations       False    -1    whatever  100
    Run Keyword And Expect Error    TypeError: speed is not an integer                         Use Object Method  ${motor}     run_for_rotations       False    -1    180       95.5
    Run Keyword And Expect Error    TypeError: seconds is not a number                         Use Object Method  ${motor}     run_for_seconds         False    -1    whatever  100
    Run Keyword And Expect Error    TypeError: speed is not an integer                         Use Object Method  ${motor}     run_for_seconds         False    -1    180       95.5
    Run Keyword And Expect Error    TypeError: speed is not an integer                         Use Object Method  ${motor}     start                   False    -1    95.5
    Run Keyword And Expect Error    TypeError: power is not an integer                         Use Object Method  ${motor}     start_at_power          False    -1    95.5
    Run Keyword And Expect Error    TypeError: degrees_counted is not an integer               Use Object Method  ${motor}     set_degrees_counted     False    -1    95.5
    Run Keyword And Expect Error    TypeError: speed is not an integer                         Use Object Method  ${motor}     set_default_speed       False    -1    95.5
    Run Keyword And Expect Error    TypeError: action is not a string                          Use Object Method  ${motor}     set_stop_action         False    -1    95.5
    Run Keyword And Expect Error    ValueError: action is not one of the allowed values        Use Object Method  ${motor}     set_stop_action         False    -1    whatever
    Run Keyword And Expect Error    TypeError: stop_when_stalled is not a boolean              Use Object Method  ${motor}     set_stall_detection     False    -1    100

8.3. Test Position Functions
    [Tags]    Motor
    Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${motor}           Create Object      Motor
    Use Object Method  ${motor}           initialize
    Play Scenario During Steps     ${motor}    50
    ${d}        Use Object Method  ${motor}    get_degrees_counted     True
    ${p}        Use Object Method  ${motor}    get_position            True
    Should Be Equal As Numbers     ${d}    64
    Should Be Equal As Numbers     ${p}    64
    Play Scenario During Steps     ${motor}    250
    ${d}        Use Object Method  ${motor}    get_degrees_counted     True
    ${p}        Use Object Method  ${motor}    get_position            True
    Should Be Equal As Numbers     ${d}    389
    Should Be Equal As Numbers     ${p}    29
    Use Object Method  ${motor}    set_degrees_counted     False    -1    0
    Play Scenario During Steps     ${motor}    41
    ${d}        Use Object Method  ${motor}    get_degrees_counted     True
    ${p}        Use Object Method  ${motor}    get_position            True
    Should Be Equal As Numbers     ${d}    54
    Should Be Equal As Numbers     ${p}    83
