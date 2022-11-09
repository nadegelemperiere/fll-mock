""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Keywords to create data for module test
# -------------------------------------------------------
# Nadège LEMPERIERE, @1 november 2022
# Latest revision: 1 november 2022
# --------------------------------------------------- """

# System includes
from threading import Thread
from time import sleep
from math import nan

# Robotframework includes
from robot.libraries.BuiltIn import BuiltIn, _Misc
from robot.api import logger as logger
from robot.api.deco import keyword
ROBOT = False

# Package includes
from spike                  import Timer, PrimeHub, ColorSensor, DistanceSensor, ForceSensor, Motor, MotorPair, wait_for_seconds, wait_until
from spike.button           import Button
from spike                  import Robot
from spike.lightmatrix      import LightMatrix
from spike.motionsensor     import MotionSensor
from spike.speaker          import Speaker
from spike.statuslight      import StatusLight
from spike.timer            import TimerSingleton

@keyword('Create Scenario')
def create_scenario(configuration) :

    result = Robot()
    result.load_configuration(configuration)
    return result

@keyword('Initialize Scenario')
def initialize_scenario(scenario, filename, sheet, object) :

    scenario.load_scenario(filename, sheet)
    scenario.initialize(object)
    return scenario

@keyword('Create Object')
def create_object(object) :

    result = None
    if object == 'Hub'                : result = PrimeHub()
    elif object == 'Button'           : result = Button()
    elif object == 'ColorSensor'      : result = ColorSensor('A')
    elif object == 'DistanceSensor'   : result = DistanceSensor('C')
    elif object == 'ForceSensor'      : result = ForceSensor('B')
    elif object == 'LightMatrix'      : result = LightMatrix()
    elif object == 'MotionSensor'     : result = MotionSensor()
    elif object == 'Motor'            : result = Motor('E')
    elif object == 'MotorPair'        :
        motor1 = Motor('E')
        motor2 = Motor('F')
        result = MotorPair('E','F')
    elif object == 'Speaker'          : result = Speaker()
    elif object == 'StatusLight'      : result = StatusLight()
    elif object == 'Timer'            : result = Timer()
    elif object == 'TimerSingleton'   : result = TimerSingleton()
    else : raise Exception('Unknown object ' + object)

    return result

@keyword('Should Have Members')
def should_have_members(object, members) :

    result = True

    content = dir(object)
    for member in members :
        if not member in content :
            raise Exception('Missing ' + member + ' in ' + str(type(object)))

    return result

@keyword('Play Scenario During Steps')
def play_scenario_during_steps(object, step) :

    for i_step in range(int(step)) :
        object.step()

@keyword('Use Object Method')
def use_object_method(object, method, shall_return=False, none_value=-1, *parameters):

    result = None

    formatted_parameters = []
    for param in parameters :
        if param.isdecimal() : formatted_parameters.append(int(param))
        elif param.replace('-','').isdecimal() : formatted_parameters.append(int(param))
        elif param.replace('.','').isdecimal() : formatted_parameters.append(float(param))
        elif param == 'True' : formatted_parameters.append(True)
        elif param == 'False' : formatted_parameters.append(False)
        else : formatted_parameters.append(param)
    formatted_parameters = tuple(formatted_parameters)

    if len(parameters) == 0 :
        if shall_return :
            result = getattr(object, method)()
        else :
            getattr(object, method)()
    else :
        if shall_return :
            result = getattr(object, method)(*formatted_parameters)
        else :
            getattr(object, method)(*formatted_parameters)

    if result is None : result = none_value
    elif isinstance(result, bool) and result : result = 'True'
    elif isinstance(result, bool) and not result : result = 'False'

    return result

@keyword('Start Method In A Thread')
def start_method_in_a_thread(object, method, *parameters):

    def thread_function(object, method, parameters):
        getattr(object, method)(*parameters)

    formatted_parameters = []
    for param in parameters :
        if param.isdecimal() : formatted_parameters.append(int(param))
        elif param.replace('.','').isdecimal() : formatted_parameters.append(float(param))
        elif param == 'True' : formatted_parameters.append(True)
        elif param == 'False' : formatted_parameters.append(False)
        else : formatted_parameters.append(param)
    formatted_parameters = tuple(formatted_parameters)

    thread = Thread(target=thread_function, args=(object, method, formatted_parameters))
    thread.start()

    return thread

@keyword('Start Function In A Thread')
def start_function_in_a_thread(function, *parameters):

    def thread_function(function, parameters):
        possibles = globals().copy()
        possibles.update(locals())
        func = possibles.get(function)
        func(*parameters)

    formatted_parameters = []
    for param in parameters :
        if param.isdecimal() : formatted_parameters.append(int(param))
        elif param.replace('.','').isdecimal() : formatted_parameters.append(float(param))
        elif param == 'True' : formatted_parameters.append(True)
        elif param == 'False' : formatted_parameters.append(False)
        else : formatted_parameters.append(param)
    formatted_parameters = tuple(formatted_parameters)

    thread = Thread(target=thread_function, args=(function, formatted_parameters))
    thread.start()

    return thread

@keyword('Is Thread Running')
def is_thread_running(thread):
    sleep(0.01)
    return thread.is_alive()
