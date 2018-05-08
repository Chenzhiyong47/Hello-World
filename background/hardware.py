#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
    Writing in newfile.py:

        from hardware import Hardware

        hardware = Hardware()

        # Press "Ctrl+C" to end a progress.
        hardware.ultrasound_A.test_distance()
        hardware.ultrasound_B.test_distance()
        hardware.ultrasound_C.test_distance()
        hardware.ultrasound_D.test_distance()

    Input in commanding script:

        python3 newfile.py

"""

import RPi.GPIO as GPIO
from time import time, sleep

GPIO.setwarnings(False)


# To control motor to start or stop.
class Motor:

    def __init__(self, Control):

        self.Control = Control
        self.init()

    def init(self):

        GPIO.setup(self.Control, GPIO.OUT, initial=GPIO.HIGH)
        sleep(0.05)

    def start(self):

        GPIO.output(self.Control, GPIO.LOW)
        sleep(0.01)

    def stop(self):

        GPIO.output(self.Control, GPIO.HIGH)
        sleep(0.01)


# To use ultrasound to measure the distance
class Ultrasound:

    def __init__(self, Trig, Echo):

        self.Trig = Trig
        self.Echo = Echo
        self.init()

    def init(self):

        GPIO.setup(self.Trig, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.Echo, GPIO.IN)
        sleep(0.08)


    '''
    这是一个超声测距模块的测量转换函数，它的原理是先向TRIG脚输入至少10us的触发信号,
    该模块内部将发出 8 个 40kHz 周期电平并检测回波。一旦检测到有回波信号则ECHO输出
    高电平回响信号。回响信号的脉冲宽度与所测的距离成正比。由此通过发射信号到收到的回
    响信号时间间隔可以计算得到距离。公式: 距离=高电平时间*声速(34000cm/S)/2。返回一个
    测量值（单位是cm）
    其中：
        t1是发现Echo脚收到高电平时的瞬时时间
        t2是发现Echo脚由高电平变为低电平时的瞬时时间
        t2-t1 就是Echo检测到高电平的时间
    '''
    def get_distance_cm(self):

        # 给TRIG脚一个12μs的高电平脉冲,发出一个触发信号
        GPIO.output(self.Trig, GPIO.HIGH)
        sleep(0.00012)
        GPIO.output(self.Trig, GPIO.LOW)
        while not GPIO.input(self.Echo):
            pass

        t1 = time()
        while GPIO.input(self.Echo):
            pass
        t2 = time()
        distance = (t2 - t1) * 34000 / 2

        return float('%.1f' % distance)

    def test(self):
        print("distance: " + str(self.get_distance_cm()))

# Object the ultrasound and motor
class Hardware:

    def __init__(self):

        self.setmode_BCM()

        # Four ultrasound: A, B, C, D
        self.ultrasound_A = Ultrasound(Trig=2, Echo=3)
        self.ultrasound_B = Ultrasound(Trig=17, Echo=27)
        self.ultrasound_C = Ultrasound(Trig=10, Echo=9)
        self.ultrasound_D = Ultrasound(Trig=5, Echo=6)

        # Four motor: A, B, C, D
        self.motor_A = Motor(Control=14)
        self.motor_B = Motor(Control=15)
        self.motor_C = Motor(Control=18)
        self.motor_D = Motor(Control=23)


    def setmode_BCM(self):

        GPIO.setmode(GPIO.BCM)


    def clearmode(self):

        GPIO.cleanup()


