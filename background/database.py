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
