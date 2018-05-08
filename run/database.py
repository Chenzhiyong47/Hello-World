from sqlalchemy import create_engine
from config import DB_URI

class database:
    def __init__(self):
        # 创建指定数据库，“echo=False”是指不支持在终端打印MySQL执行的过程
        self.engine = create_engine(DB_URI, echo=False)

    # 通过原生语句直接操作数据库
    # 增
    def insert_data_by_commands(self, commands):
        with self.engine.connect() as con:
            con.execute(commands)

    # 删
    def delete_data_by_commands(self, commands):
        with self.engine.connect() as con:
            con.execute(commands)

    # 查
    def get_data_by_commands(self, commands):
        with self.engine.connect() as con:
            the_data = con.execute(commands)
            # print(type(the_data))
        return the_data

    # 改
    def modify_data_by_commands(self, commands):
        with self.engine.connect() as con:
            con.execute(commands)

    # create table
    def create_table_by_commands(self, commands):
        with self.engine.connect() as con:
            con.execute(commands)

    # drop tables
    def drop_table_by_commands(self, commands):
        with self.engine.connect() as con:
            con.execute(commands)


class operate_database:
    def __init__(self):
        self.database = database()

    # attain data from db
    def get_motor_status_and_command_from_db(self, which_motor):

        motor_status = None
        motor_command = None
        commands = "Select * From motor Where motor='{which_motor}';".format(
                    which_motor=which_motor)
        data = self.database.get_data_by_commands(commands)

        for i in data:
            motor_status = i[2]
            motor_command = i[3]

        return motor_status, motor_command

    def get_setting_distance_from_db(self, which_ultrasound):

        setting_distance = None
        commands = "Select * From {which_ultra} Where ID=2;".format(
                    which_ultra=which_ultrasound)
        data = self.database.get_data_by_commands(commands)

        for i in data:
            setting_distance = i[2]

        return setting_distance

    def get_newest_distance_from_db(self, which_ultrasound):

        newest_distance = None
        commands = "Select * From {which_ultra} Order By ID Desc Limit 1;".format(
                    which_ultra=which_ultrasound)

        data = self.database.get_data_by_commands(commands)

        for i in data:
            newest_distance = i[2]

        return newest_distance

    def get_newest_time_and_dist_from_db(self, which_ultrasound):

        newest_time = None
        newest_distance = None
        commands = "Select * From {which_ultra} Order By ID Desc Limit 1;".format(
                    which_ultra=which_ultrasound)

        data = self.database.get_data_by_commands(commands)

        for i in data:
            newest_time = i[1]
            newest_distance = i[2]

        return newest_time, newest_distance


    # update data of db
    def update_motor_command_in_db(self, which_motor, command):
        commands = "Update motor Set Command='{command}' Where Motor='{which_motor}'".format(
                    command=command, which_motor=which_motor)

        self.database.modify_data_by_commands(commands)

    def update_setting_distance_in_db(self, which_ultrasound, setting_distance):
        commands = "Update {which_ultrasound} Set distance={setting_distance} Where ID=2".format(
                    which_ultrasound=which_ultrasound, setting_distance=setting_distance)

        self.database.modify_data_by_commands(commands)





