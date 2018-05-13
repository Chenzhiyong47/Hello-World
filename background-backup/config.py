# debug
DEBUG = True


# DB settings
# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = ''
HOST = '127.0.0.1'
PORT = 3306
# 数据库名称为'time_distance'
DATABASE = 'time_distance'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,
                        DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

DB_URI = SQLALCHEMY_DATABASE_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False


