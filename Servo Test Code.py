import time
import board
import pulseio
from adafruit_motor import servo

true90top = 97
true90bottom = 87
# create a PWMOut object on Pin A2.
d10 = pulseio.PWMOut(board.D10, duty_cycle=2 ** 15, frequency=50)
d11 = pulseio.PWMOut(board.D11, duty_cycle=2 ** 15, frequency=50)
d9 = pulseio.PWMOut(board.D9, duty_cycle=2 ** 15, frequency=50)
d7 = pulseio.PWMOut(board.D7, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
LT = servo.Servo(d11)
LB = servo.Servo(d10)
RT = servo.Servo(d9)
RB = servo.Servo(d7)

'''
Turns the robot to the left
'''


def resetServo():
    LT.angle = true90top
    time.sleep(0.5)
    RT.angle = true90top
    time.sleep(0.5)
    LB.angle = true90bottom
    time.sleep(0.5)
    RB.angle = true90bottom
    time.sleep(0.5)


def turnLeft():
    for angle in range(true90top, 130, 10):
        RT.angle = angle
        time.sleep(0.5)
    for angle in reversed(range(50, true90bottom, 10)):
        RB.angle = angle
        time.sleep(0.5)
    for angle in range(50, true90bottom, 10):
        RB.angle = angle
        time.sleep(0.5)
    for angle in reversed(range(130, true90top, 10)):
        RT.angle = angle
        time.sleep(0.5)


'''
Turns the robot to the right
'''


def turnRight():
    for angle in reversed(range(70, true90top, 10)):
        LT.angle = angle
        time.sleep(0.5)
    for angle in reversed(range(50, true90bottom, 10)):
        LB.angle = angle
        time.sleep(0.5)
    for angle in range(50, true90bottom, 10):
        LB.angle = angle
        time.sleep(0.5)
    for angle in range(70, true90top, 10):
        LT.angle = angle
        time.sleep(0.5)


def Move1():
    for angle in range(true90top, 57, 10):
        RB.angle = angle
        time.sleep(0.5)
    for angle in range(true90top, 57, 10):
        LB.angle = angle
        time.sleep(0.5)
    for i in range(10):
        for angle in range(true90bottom, 57, 10):
            LT.angle = angle
            time.sleep(0.5)
    RB.angle = true90bottom
    LB.angle = true90bottom
    RT.angle = true90top
    LT.angle = true90top


def Move2():
    LB.angle = true90bottom + 57
    RB.angle = true90bottom - 57
    time.sleep(0.5)
    LB.angle = true90bottom
    RB.angle = true90bottom
    time.sleep(0.5)
    LB.angle = true90bottom - 57
    RB.angle = true90bottom + 57
    time.sleep(0.5)
    LB.angle = true90bottom
    RB.angle = true90bottom
    time.sleep(0.5)
    LB.angle = true90bottom - 50
    LT.angle = true90top + 40
    time.sleep(0.5)
    LB.angle = true90bottom
    LT.angle = true90top
    time.sleep(0.5)
    RB.angle = true90bottom + 50
    RT.angle = true90top - 40
    time.sleep(0.5)
    RB.angle = true90bottom
    RT.angle = true90top
    time.sleep(0.5)
    resetServo()


def Move3():
    RB.angle = 110
    time.sleep(0.5)
    LB.angle = 140
    time.sleep(0.5)
    for angle in range(true90top, 140, 10):
        RT.angle = angle
        time.sleep(0.5)
    time.sleep(0.5)
    RT.angle = true90top
    time.sleep(0.5)
    resetServo()

resetServo()