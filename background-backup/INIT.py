# -*- coding: utf-8 -*-
# The codes' function is to set the Initialized database
#   Initialize the database 'motor':
#       ID    Motor     Status      Command
#       1      A        stop         stop
#       2      B        stop         stop
#       3      C        stop         stop
#       4      D        stop         stop
#   Initialize database ultrasound_A(B, C, D):
#       ID        time       distance
#       1         NULL        reality       # distance to bottom of barrel
#       2         NULL      reality / 2     # half of the distance to bottom of barrel
#       3       real time     reality       # ID (3 to n) is record the real distance



import time
from database import database
from hardware import Hardware

database = database()
hardware = Hardware()
ultrasound = {'A': hardware.ultrasound_A.get_distance_cm(),
              'B': hardware.ultrasound_B.get_distance_cm(),
              'C': hardware.ultrasound_C.get_distance_cm(),
              'D': hardware.ultrasound_D.get_distance_cm()}

# get the distance of ultrasound
def get_distance(get_which_ultra_dist):

    distance = 0.0

    for i in range(4):
        distance += get_which_ultra_dist
        time.sleep(0.15)

    return distance / 4


def create_table(Table, Data_and_Type):
    create_command = "Create Table {table} ({data_and_type});".format(
                table=Table, data_and_type=Data_and_Type)

    return create_command

def drop_table(Table):
    drop_command = "Drop Table If Exists {table};".format(table=Table)

    return drop_command

def delete_line(Table, Which_line):
    delete_command = "Delete From {table} Where {which_line};".format(
            table=Table, which_line=Which_line)

    return delete_command

def insert_line(Table, Members, Values):
    insert_command = "Insert Into {table}({members})Values({values});".format(
            table=Table, members=Members, values=Values)

    return insert_command



# initialize tables begin
def init_tables():
    motor = 'motor'
    ultrasound_A = 'ultrasound_A'
    ultrasound_B = 'ultrasound_B'
    ultrasound_C = 'ultrasound_C'
    ultrasound_D = 'ultrasound_D'

    motor_data_and_type = "	ID        TINYINT       NOT NULL AUTO_INCREMENT," +\
	                      " Motor     CHAR(1)       NULL," +\
	                      " Status    CHAR(5)       NULL," +\
	                      " Command   CHAR(5)       NULL," +\
	                      " PRIMARY KEY  (ID)"

    ultrasound_data_and_type = "ID           int           NOT NULL  AUTO_INCREMENT," +\
		                       "time         TIMESTAMP     NULL,"  +\
		                       "distance     FLOAT(5,1)    NULL," +\
		                       "PRIMARY KEY  (ID)"

    # drop tables
    database.drop_table_by_commands(drop_table(motor))
    database.drop_table_by_commands(drop_table(ultrasound_A))
    database.drop_table_by_commands(drop_table(ultrasound_B))
    database.drop_table_by_commands(drop_table(ultrasound_C))
    database.drop_table_by_commands(drop_table(ultrasound_D))

    # create tables
    database.create_table_by_commands(create_table(motor, motor_data_and_type))
    database.create_table_by_commands(create_table(ultrasound_A, ultrasound_data_and_type))
    database.create_table_by_commands(create_table(ultrasound_B, ultrasound_data_and_type))
    database.create_table_by_commands(create_table(ultrasound_C, ultrasound_data_and_type))
    database.create_table_by_commands(create_table(ultrasound_D, ultrasound_data_and_type))

init_tables()
# Initialize tables end



# Initialize database 'motor' begin
def init_motor():

    motor = 'motor'
    motor_A = "motor = 'A'"
    motor_B = "motor = 'B'"
    motor_C = "motor = 'C'"
    motor_D = "motor = 'D'"

    members = "ID, Motor, Status, Command"
    values_A = "'1', 'A', 'stop', 'auto'"
    values_B = "'2', 'B', 'stop', 'auto'"
    values_C = "'3', 'C', 'stop', 'auto'"
    values_D = "'4', 'D', 'stop', 'auto'"

    # delete old lines
    database.delete_data_by_commands(delete_line(motor, motor_A))
    database.delete_data_by_commands(delete_line(motor, motor_B))
    database.delete_data_by_commands(delete_line(motor, motor_C))
    database.delete_data_by_commands(delete_line(motor, motor_D))

    # insert new line
    database.insert_data_by_commands(insert_line(motor, members, values_A))
    database.insert_data_by_commands(insert_line(motor, members, values_B))
    database.insert_data_by_commands(insert_line(motor, members, values_C))
    database.insert_data_by_commands(insert_line(motor, members, values_D))

init_motor()
# Initialize database 'motor' ends



# Initialize database 'ultrasound_A(B, C, D)' begins
def init_ultrasound(ultrasound, real_distance):

    ultrasound = ultrasound
    # distance to bottom of barrel
    ID_1 = "ID=1"
    # half of the distance to bottom of barrel
    ID_2 = "ID=2"

    members = "ID, time, distance"
    values_1 = "1, NULL, {real}".format(real=real_distance)
    values_2 = "2, NULL, {real}".format(real=real_distance/2)

    # delete old lines
    database.delete_data_by_commands(delete_line(ultrasound, ID_1))
    database.delete_data_by_commands(delete_line(ultrasound, ID_2))

    # insert new lines
    database.insert_data_by_commands(insert_line(ultrasound, members, values_1))
    database.insert_data_by_commands(insert_line(ultrasound, members, values_2))

init_ultrasound("ultrasound_A", get_distance(ultrasound['A']))
init_ultrasound("ultrasound_B", get_distance(ultrasound['B']))
init_ultrasound("ultrasound_C", get_distance(ultrasound['C']))
init_ultrasound("ultrasound_D", get_distance(ultrasound['D']))
# Initialize database 'ultrasound_A(B, C, D)' ends



