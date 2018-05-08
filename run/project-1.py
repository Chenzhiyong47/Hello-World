from flask import Flask, render_template, request, jsonify
from flask_script import Manager
import database
import json
import config

app = Flask(__name__)
app.config.from_object(config)
manager = Manager(app)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/figure')
def figure():
    return render_template("figure.html")

@app.route('/test')
def test():
    return render_template("test.html")



DATABASE = database.operate_database()


# ################### get the data to display in web ##################

@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    print("get data     post")
    Get_Data = {}

    if request.method == 'POST':
        the_data = request.form['get_data']
        print(the_data)
        print('getting data from db now')

        motor_A_status, motor_A_command = DATABASE.get_motor_status_and_command_from_db('A')
        motor_B_status, motor_B_command = DATABASE.get_motor_status_and_command_from_db('B')
        motor_C_status, motor_C_command = DATABASE.get_motor_status_and_command_from_db('C')
        motor_D_status, motor_D_command = DATABASE.get_motor_status_and_command_from_db('D')

        ultra_A_dist = DATABASE.get_newest_distance_from_db("ultrasound_A")
        ultra_B_dist = DATABASE.get_newest_distance_from_db("ultrasound_B")
        ultra_C_dist = DATABASE.get_newest_distance_from_db("ultrasound_C")
        ultra_D_dist = DATABASE.get_newest_distance_from_db("ultrasound_D")

        setting_A_dist = DATABASE.get_setting_distance_from_db("ultrasound_A")
        setting_B_dist = DATABASE.get_setting_distance_from_db("ultrasound_B")
        setting_C_dist = DATABASE.get_setting_distance_from_db("ultrasound_C")
        setting_D_dist = DATABASE.get_setting_distance_from_db("ultrasound_D")

        Get_Data = {
            "motor_A_status": motor_A_status,
            "motor_B_status": motor_B_status,
            "motor_C_status": motor_C_status,
            "motor_D_status": motor_D_status,

            "ultra_A_dist": ultra_A_dist,
            "ultra_B_dist": ultra_B_dist,
            "ultra_C_dist": ultra_C_dist,
            "ultra_D_dist": ultra_D_dist,

            "setting_A_dist": setting_A_dist,
            "setting_B_dist": setting_B_dist,
            "setting_C_dist": setting_C_dist,
            "setting_D_dist": setting_D_dist
            }

        print(Get_Data)

    return jsonify(Get_Data)


@app.route('/get_time_distance', methods=['GET', 'POST'])
def get_time_distance():
    print("get_time_distance    post")
    Get_Time_Distance = {}

    if request.method == 'POST':
        the_data = request.form["get_time_distance"]
        print(the_data)
        print('getting data from db now')

        time_A, distance_A = DATABASE.get_newest_time_and_dist_from_db("ultrasound_A")
        time_B, distance_B = DATABASE.get_newest_time_and_dist_from_db("ultrasound_B")
        time_C, distance_C = DATABASE.get_newest_time_and_dist_from_db("ultrasound_C")
        time_D, distance_D = DATABASE.get_newest_time_and_dist_from_db("ultrasound_D")

        Get_Time_Distance = {
                             "time_A": time_A,
                             "time_B": time_B,
                             "time_C": time_C,
                             "time_D": time_D,

                             "distance_A": distance_A,
                             "distance_B": distance_B,
                             "distance_C": distance_C,
                             "distance_D": distance_D
                            }

    return jsonify(Get_Time_Distance)


#########################  motor controlling  ###########################

def MOTOR(motor):
    motor_status, motor_command = DATABASE.get_motor_status_and_command_from_db(motor)

    motor_order = request.args.get("motor_order")

    if (motor_command != "stop") and (motor_order == "stop"):
        DATABASE.update_motor_command_in_db(motor, 'stop')
        motor_status = motor_order

    elif (motor_command != "start") and (motor_order == "start"):
        DATABASE.update_motor_command_in_db(motor, 'start')
        motor_status = motor_order

    elif (motor_command != 'auto') and (motor_order == 'auto'):
        DATABASE.update_motor_command_in_db(motor, 'auto')


    else:
        pass

    return motor_status


@app.route('/motor_A')
def motor_A(motor='A'):

    r_m = MOTOR(motor)

    return r_m

@app.route('/motor_B')
def motor_B(motor='B'):

    r_m = MOTOR(motor)

    return r_m

@app.route('/motor_C')
def motor_C(motor='C'):

    r_m = MOTOR(motor)

    return r_m

@app.route('/motor_D')
def motor_D(motor='D'):

    r_m = MOTOR(motor)

    return r_m


def ultra_setting_dist(ultrasound):
    distance = request.args.get('setting_distance')
    DATABASE.update_setting_distance_in_db(ultrasound, distance)

    return "success to modify"

@app.route('/ultrasound_A_setting')
def ultrasound_A_setting(ultrasound="ultrasound_A"):
    r_u = ultra_setting_dist(ultrasound)

    return r_u


@app.route('/ultrasound_B_setting')
def ultrasound_B_setting(ultrasound="ultrasound_B"):
    r_u = ultra_setting_dist(ultrasound)

    return r_u


@app.route('/ultrasound_C_setting')
def ultrasound_C_setting(ultrasound="ultrasound_C"):
    r_u = ultra_setting_dist(ultrasound)

    return r_u


@app.route('/ultrasound_D_setting')
def ultrasound_D_setting(ultrasound="ultrasound_D"):
    r_u = ultra_setting_dist(ultrasound)

    return r_u


if __name__ == '__main__':
    manager.run()
