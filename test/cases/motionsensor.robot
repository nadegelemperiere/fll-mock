# -------------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Robotframework test suite to test spike motion sensor mock
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# -------------------------------------------------------

*** Settings ***
Documentation   A test case to check motion sensor mock functioning
Library         ../keywords/objects.py
Library         Collections

*** Variables ***
${JSON_CONF_FILE}                 ${data}/truth.json
${EXCEL_DATA_FILE}                ${data}/motion-sensor-scenarii.xlsx

*** Test Cases ***

7.1 Ensure Motion Sensor Is Created With The Required Constants
    [Tags]      MotionSensor
    Create Scenario  ${JSON_CONF_FILE}    ${EXCEL_DATA_FILE}    simple
    ${sensor}        Create Object  MotionSensor
    @{members} =     Create List    get_yaw_angle    get_pitch_angle    get_roll_angle    get_orientation    get_gesture     was_gesture    reset_yaw_angle    wait_for_new_gesture     wait_for_new_orientation
    Should Have Members    ${sensor}    ${members}

7.2 Ensure Error Management Is Correctly Implemented
    [Tags]      MotionSensor
    Create Scenario  ${JSON_CONF_FILE}    ${EXCEL_DATA_FILE}    simple
    ${sensor}        Create Object  MotionSensor
    Run Keyword And Expect Error    ValueError: Invalid gesture : 'gesture'   Use Object Method  ${sensor}     was_gesture    True    -1     'gesture'

7.3 Test Motion Sensor Behavior On Simple Scenario
    [Tags]      MotionSensor
    ${scenario}         Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${sensor}           Create Object      MotionSensor
    Use Object Method   ${sensor}          initialize
    @{steps} =          Create List    10        11      6          9       9         9        8       10      27      5
    @{yaw} =            Create List    0         30      90         180     -90       0        0       0       0       0
    @{pitch} =          Create List    0         0       0          0       0         0        50      -50     0       0
    @{roll} =           Create List    0         0       0          0       0         0        0       0       120     -65
    @{gesture} =        Create List    ${EMPTY}  tapped  tapped     tapped  falling   falling  shaken  shaken  shaken  shaken
    @{orientation} =    Create List    front     front   rightside  back    leftside  front    up      down    front   front
    ${i_step} =         Set Variable   0
    ${i_step} =         Convert To Integer  ${i_step}
    FOR    ${step}    IN    @{steps}
        Play Scenario During Steps     ${sensor}    ${step}
        ${y}        Use Object Method  ${sensor}    get_yaw_angle    True
        ${p}        Use Object Method  ${sensor}    get_pitch_angle  True
        ${r}        Use Object Method  ${sensor}    get_roll_angle   True
        ${g}        Use Object Method  ${sensor}    get_gesture      True
        ${o}        Use Object Method  ${sensor}    get_orientation  True
        ${yt}       Get From List      ${yaw}            ${i_step}
        ${pt}       Get From List      ${pitch}          ${i_step}
        ${rt}       Get From List      ${roll}           ${i_step}
        ${gt}       Get From List      ${gesture}        ${i_step}
        ${ot}       Get From List      ${orientation}    ${i_step}
        Should Be Equal As Integers    ${yt}     ${y}
        Should Be Equal As Integers    ${pt}     ${p}
        Should Be Equal As Integers    ${yt}     ${y}
        Should Be Equal                ${gt}     ${g}
        Should Be Equal                ${ot}     ${o}
        ${i_step} =     Set Variable   ${i_step + 1}
    END

7.4 Test Yaw Reset Function Behaviour
    [Tags]  MotionSensor
    ${scenario}         Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${sensor}           Create Object      MotionSensor
    Use Object Method   ${sensor}          initialize
    Play Scenario During Steps     ${sensor}  0
    ${y}        Use Object Method  ${sensor}  get_yaw_angle  True
    Should Be Equal As Integers    ${y}       0
    Play Scenario During Steps     ${sensor}  130
    ${y}        Use Object Method  ${sensor}  get_yaw_angle  True
    Should Be Equal As Integers    ${y}       120
    ${y}        Use Object Method  ${sensor}  reset_yaw_angle  True
    ${y}        Use Object Method  ${sensor}  get_yaw_angle  True
    Should Be Equal As Integers    ${y}       0
    Play Scenario During Steps     ${sensor}  10
    ${y}        Use Object Method  ${sensor}  get_yaw_angle  True
    Should Be Equal As Integers    ${y}       0
    Play Scenario During Steps     ${sensor}  80
    ${y}        Use Object Method  ${sensor}  get_yaw_angle  True
    Should Be Equal As Integers    ${y}       -120

7.5 Test 'was_gesture' Behaviour
    [Tags]  MotionSensor
    ${scenario}         Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${sensor}           Create Object      MotionSensor
    Use Object Method   ${sensor}          initialize
    @{steps} =          Create List    10    10      5     45       5
    @{values} =         Create List    none  tapped  none  falling  falling
    @{results} =        Create List    True  True    True  True     False
    ${i_step} =         Set Variable   0
    ${i_step} =         Convert To Integer  ${i_step}
    FOR    ${step}    IN    @{steps}
        Play Scenario During Steps     ${sensor}    ${step}
        ${value}    Get From List      ${values}    ${i_step}
        ${r}        Use Object Method  ${sensor}    was_gesture    True    -1    ${value}
        ${rt}       Get From List      ${results}        ${i_step}
        Should Be Equal                ${r}     ${rt}
        ${i_step} =     Set Variable   ${i_step + 1}
    END

7.6 Test The Parallel Behaviour Of Wait functions
    [Tags]  MotionSensor
    ${scenario}         Create Scenario    ${JSON_CONF_FILE}  ${EXCEL_DATA_FILE}    simple
    ${sensor}           Create Object      MotionSensor
    Use Object Method   ${sensor}          initialize
    Play Scenario During Steps  ${sensor}      10
    ${thread}           Start Method In A Thread    ${sensor}    wait_for_new_gesture
    ${is_alive}         Is Thread Running      ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}      20
    ${is_alive}         Is Thread Running      ${thread}
    Should Not Be True  ${is_alive}
    ${thread}           Start Method In A Thread    ${sensor}    wait_for_new_orientation
    ${is_alive}         Is Thread Running      ${thread}
    Should Be True      ${is_alive}
    Play Scenario During Steps  ${sensor}      20
    ${is_alive}         Is Thread Running      ${thread}
    Should Not Be True  ${is_alive}

