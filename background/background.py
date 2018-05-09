# -*- coding: utf-8 -*-

import time
from database import database
from hardware import Hardware


database = database()
hardware = Hardware()

ultrasound_A = "ultrasound_A"
ultrasound_B = "ultrasound_B"
ultrasound_C = "ultrasound_C"
ultrasound_D = "ultrasound_D"

motor_A = 'A'
motor_B = 'B'
motor_C = 'C'
motor_D = 'D'


class ultrasound:

    def __init__(self):
        pass

    def get_A_distance(self):
        return hardware.ultrasound_A.get_distance_cm()

    def get_B_distance(self):
        return hardware.ultrasound_B.get_distance_cm()

    def get_C_distance(self):
        return hardware.ultrasound_C.get_distance_cm()

    def get_D_distance(self):
        return hardware.ultrasound_D.get_distance_cm()

ULTRASOUND = ultrasound()


def get_motor_status_and_command_from_db(which_motor):

    motor_status = None
    motor_command = None
    commands = "Select * From motor Where motor='{which_motor}';".format(
                which_motor=which_motor)
    data = database.get_data_by_commands(commands)

    for i in data:
        motor_status = i[2]
        motor_command = i[3]

    return motor_status, motor_command


def update_motor_status_in_db(which_motor, status):
    commands = "Update motor Set Status='{status}' Where Motor='{which_motor}'".format(
                status=status, which_motor=which_motor)

    database.modify_data_by_commands(commands)


# get the setting distance of each ultrasound
def get_setting_distance_from_db(which_ultrasound):

    setting_distance = None
    commands = "Select * From {which_ultra} Where ID=2;".format(
                which_ultra=which_ultrasound)
    data = database.get_data_by_commands(commands)

    for i in data:
        setting_distance = i[2]

    return setting_distance
    
# get the setting distance of each ultrasound
def get_inited_distance_from_db(which_ultrasound):

    inited_distance = None
    commands = "Select * From {which_ultra} Where ID=1;".format(
                which_ultra=which_ultrasound)
    data = database.get_data_by_commands(commands)

    for i in data:
        inited_distance = i[2]

    return inited_distance


# get the newest distance of each ultrasound
def get_newest_distance_from_db(which_ultrasound):

    newest_distance = None
    commands = "Select * From {which_ultra} Order By ID Desc Limit 1;".format(
                which_ultra=which_ultrasound)

    data = database.get_data_by_commands(commands)

    for i in data:
        newest_distance = i[2]

    return newest_distance


def get_real_time():

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def insert_real_distance_to_db(which_ultrasound, Time=None, Distance=None):

    commands = "Insert Into {table}(time, distance)Values('{Time}', {Distance});".format(
            table=which_ultrasound, Time=Time, Distance=Distance)

    database.insert_data_by_commands(commands)


inited_A_distance = get_inited_distance_from_db(ultrasound_A)
inited_B_distance = get_inited_distance_from_db(ultrasound_B)
inited_C_distance = get_inited_distance_from_db(ultrasound_C)
inited_D_distance = get_inited_distance_from_db(ultrasound_D)


class cascading:
    def __init__(self):
        # get A, B, C, Ds' setting distance
        pass
        

    def cascading_A(self):
        insert_real_distance_to_db(ultrasound_A, get_real_time(), inited_A_distance - ULTRASOUND.get_A_distance())
        time.sleep(0.6)
        motor_status, motor_command = get_motor_status_and_command_from_db(motor_B)

        if motor_command == 'stop':
            hardware.motor_B.stop()
            time.sleep(0.1)
            update_motor_status_in_db(motor_B, 'stop')

        elif motor_command == 'start':
            hardware.motor_B.start()
            time.sleep(0.1)
            update_motor_status_in_db(motor_B, 'start')

        elif motor_command == 'auto':

            if get_newest_distance_from_db(ultrasound_A) < get_setting_distance_from_db(ultrasound_A):
                print("B_start")
                update_motor_status_in_db(motor_B, 'start')
                hardware.motor_B.start()
                time.sleep(0.1)

            elif get_newest_distance_from_db(ultrasound_A) > get_setting_distance_from_db(ultrasound_A):
                print("B_stop")
                update_motor_status_in_db(motor_B, 'stop')
                hardware.motor_B.stop()
                time.sleep(0.1)

    def cascading_B(self):
        insert_real_distance_to_db(ultrasound_B, get_real_time(), inited_B_distance - ULTRASOUND.get_B_distance())
        time.sleep(0.6)
        motor_status, motor_command = get_motor_status_and_command_from_db(motor_C)

        if motor_command == 'stop':
            hardware.motor_C.stop()
            time.sleep(0.1)
            update_motor_status_in_db(motor_C, 'stop')

        elif motor_command == 'start':
            hardware.motor_C.start()
            time.sleep(0.1)
            update_motor_status_in_db(motor_C, 'start')

        elif motor_command == 'auto':

            if get_newest_distance_from_db(ultrasound_B) < get_setting_distance_from_db(ultrasound_B):
                print("C_start")
                update_motor_status_in_db(motor_C, 'start')
                hardware.motor_C.start()
                time.sleep(0.1)

            elif get_newest_distance_from_db(ultrasound_B) > get_setting_distance_from_db(ultrasound_B):
                print("C_stop")
                update_motor_status_in_db(motor_C, 'stop')
                hardware.motor_C.stop()
                time.sleep(0.1)

    def cascading_C(self):
        insert_real_distance_to_db(ultrasound_C, get_real_time(), inited_C_distance - ULTRASOUND.get_C_distance())
        time.sleep(0.6)
        motor_status, motor_command = get_motor_status_and_command_from_db(motor_D)

        if motor_command == 'stop':
            hardware.motor_D.stop()
            time.sleep(0.1)
            update_motor_status_in_db(motor_D, 'stop')

        elif motor_command == 'start':
            hardware.motor_D.start()
            time.sleep(0.1)
            update_motor_status_in_db(motor_D, 'start')

        elif motor_command == 'auto':

            if get_newest_distance_from_db(ultrasound_C) < get_setting_distance_from_db(ultrasound_C):
                print("D_start")
                update_motor_status_in_db(motor_D, 'start')
                hardware.motor_D.start()
                time.sleep(0.1)

            elif get_newest_distance_from_db(ultrasound_C) > get_setting_distance_from_db(ultrasound_C):
                print("D_stop")
                update_motor_status_in_db(motor_D, 'stop')
                hardware.motor_D.stop()
                time.sleep(0.1)

    def cascading_D(self):
        insert_real_distance_to_db(ultrasound_D, get_real_time(), inited_C_distance - ULTRASOUND.get_D_distance())

        if get_newest_distance_from_db(ultrasound_D) < get_setting_distance_from_db(ultrasound_D):
            print("water is little")

        elif get_newest_distance_from_db(ultrasound_D) > get_setting_distance_from_db(ultrasound_D):
            print("water is enough")

cascading = cascading()

try:
    while(1):
        cascading.cascading_A()
        cascading.cascading_B()
        cascading.cascading_C()
        cascading.cascading_D()


except KeyboardInterrupt:
    print('end!')
