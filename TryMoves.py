import time
import board
import pulseio
from adafruit_motor import servo

# SERVO ORIENTATION

# BOTTOMS / towards 0, \ towards 180
# TOPS Counter clockwise towards 0 (right leg in, left leg out), v.v for 180

# calibrated angle for the leg
true90top = 97
true90bottom = 87

# create a PWMOut object on Pin A2.
d10 = pulseio.PWMOut(board.D10, duty_cycle=2 ** 15, frequency=50)
d11 = pulseio.PWMOut(board.D11, duty_cycle=2 ** 15, frequency=50)
d9 = pulseio.PWMOut(board.D9, duty_cycle=2 ** 15, frequency=50)
d7 = pulseio.PWMOut(board.D7, duty_cycle=2 ** 15, frequency=50)

# Create a servo object, my_servo.
LT = servo.Servo(d11)
LB = servo.Servo(d9)
RT = servo.Servo(d10)
RB = servo.Servo(d7)


# reset servos to their default angle.
def resetServo():
    LT.angle = true90top
    time.sleep(0.5)
    RT.angle = true90top
    time.sleep(0.5)
    LB.angle = true90bottom
    time.sleep(0.5)
    RB.angle = true90bottom
    time.sleep(0.5)


# class for Move
class Move:
    # class will have 3 attributes. limb, angle, duration of sleep between moves
    def __init__(self, limb, degree, duration):
        self.limb = limb
        self.degree = degree
        self.duration = duration


# set limbs to default angle
LB_reset = Move(LB, true90bottom, 0.05)
RB_reset = Move(RB, true90bottom, 0.05)
LT_reset = Move(LT, true90top, 0.05)
RT_reset = Move(RT, true90top, 0.05)
# individual moves for our Move1
mov1_1 = Move(LB, true90bottom + 47, 0.001)
mov1_2 = Move(RB, true90bottom - 47, 0.20)
mov1_3 = Move(LB, true90bottom - 47, 0.001)
mov1_4 = Move(RB, true90bottom + 47, 0.20)
mov1_5 = Move(LB, true90bottom - 30, 0.001)
mov1_6 = Move(LT, true90top + 30, 0.20)
mov1_7 = Move(RB, true90bottom + 30, 0.001)
mov1_8 = Move(RT, true90top - 30, 0.20)

mov1_9 = Move(LB, true90bottom + 30, 0.001)
mov1_10 = Move(LT, true90top - 30, 0.20)
mov1_11 = Move(RB, true90bottom - 30, 0.001)
mov1_12 = Move(RT, true90top + 30, 0.20)

# complete list for Move1
Move1 = [mov1_1, mov1_2, LB_reset, RB_reset, mov1_3, mov1_4, LB_reset, RB_reset,
         mov1_5, mov1_6, LB_reset, LT_reset, mov1_7, mov1_8, RB_reset, RT_reset,
         mov1_9, mov1_10, LB_reset, LT_reset, mov1_11, mov1_12, RB_reset, RT_reset]
# copy of Move1
Move1_copy = [mov1_1, mov1_2, LB_reset, RB_reset, mov1_3, mov1_4, LB_reset, RB_reset,
              mov1_5, mov1_6, LB_reset, LT_reset, mov1_7, mov1_8, RB_reset, RT_reset,
              mov1_9, mov1_10, LB_reset, LT_reset, mov1_11, mov1_12, RB_reset, RT_reset]


# Move No.2 : Wave
def wave_move():
    vertical_list = []
    angle = true90bottom
    for i in range(1, 7):
        vertical_list.append(Move(LB, angle - 10 * i, 0.05))
    for i in range(1, 8):
        vertical_list.append(Move(LB, angle + 10 * i, 0.01))
    for i in range(1, 7):
        vertical_list.append(Move(RB, angle + 10 * i, 0.05))
    for i in range(1, 8):
        vertical_list.append(Move(RB, angle - 10 * i, 0.01))
    return vertical_list


# Move2 as a list
wave = wave_move()
wave_copy = wave_move()

# Move No.3 : Dab
def dab_move():
    result = []
    rightbot = true90bottom
    righttop = true90top
    leftbot = true90bottom
    lefttop = true90top
    for i in range (1, 7):
        result.append(Move(RB, rightbot - 10 * i, 0.02))
    rightbot -= 60
    for i in range (1, 7):
        result.append(Move(RT, righttop - 10 * i, 0.02))
    righttop -= 60
    for i in range (1, 7):
        result.append(Move(LT, lefttop - 10 * i, 0.02))
    lefttop -= 60
    for i in range (1, 7):
        result.append(Move(RB, rightbot + 10 * i, 0.02))
    rightbot = true90bottom
    for i in range(1, 7):
        result.append(Move(LB, leftbot - 10 * i, 0.02))
    leftbot -= 60

    for i in range(1, 7):
        result.append(Move(LB, leftbot + 10 * i, 0.02))
    leftbot = true90bottom

    # second dab
    for i in range(1, 7):
        result.append(Move(LB, leftbot - 10 * i, 0.02))
    leftbot -= 60
    for i in range(1, 7):
        result.append(Move(LB, leftbot + 10 * i, 0.02))
    leftbot = true90bottom



    for i in range(1, 7):
        result.append(Move(LT, lefttop + 10 * i, 0.02))
    lefttop = true90top
    for i in range(1, 7):
        result.append(Move(RT, righttop + 10 * i, 0.02))
    righttop = true90top
    # dab on the other side
    for i in range (1, 7):
        result.append(Move(LB, leftbot + 10 * i, 0.02))
    leftbot += 60
    for i in range (1, 7):
        result.append(Move(LT, lefttop + 10 * i, 0.02))
    lefttop += 60
    for i in range (1, 7):
        result.append(Move(RT, righttop + 10 * i, 0.02))
    righttop += 60
    for i in range (1, 7):
        result.append(Move(LB, leftbot - 10 * i, 0.02))
    leftbot = true90bottom
    for i in range(1, 7):
        result.append(Move(RB, rightbot + 10 * i, 0.02))
    rightbot += 60

    for i in range(1, 7):
        result.append(Move(RB, rightbot - 10 * i, 0.02))
    rightbot = true90bottom
    
    # second dab
    for i in range(1, 7):
        result.append(Move(RB, rightbot + 10 * i, 0.02))
    rightbot += 60
    for i in range(1, 7):
        result.append(Move(RB, rightbot - 10 * i, 0.02))
    rightbot = true90bottom


    for i in range(1, 7):
        result.append(Move(RT, righttop - 10 * i, 0.02))
    righttop = true90top
    for i in range(1, 7):
        result.append(Move(LT, lefttop - 10 * i, 0.02))
    lefttop = true90top
    return result

dab = dab_move()
dab_copy = dab_move()


# Move No.4 : Turn Left
def turn_left():
    result = [Move(LT, 40, 0.1), Move(RT, 110, 0.1), Move(RB, 70, 0.1)]
    for i in range(5):
        for ang in range(40, true90bottom, 10):
            result.append(Move(LB, ang, 0.005))
            result.append(Move(LT, ang, 0.05))
    return result


# Move4 as a list
turnLeft = turn_left()
turnLeftCopy = turn_left()


# Move No.5 : Turn Right
def turn_Right():
    result = [Move(RT, 140, 0.1), Move(LT, 70, 0.1), Move(LB, 110, 0.1)]
    for i in range(5):

        for ang in reversed(range(90, 130, 10)):
            result.append(Move(RB, ang, 0.005))
            result.append(Move(RT, ang, 0.05))
    return result


# Move5 as a list
turnRight = turn_Right()
turnRightCopy = turn_Right()


# Move No.6 : Humping
def humping():
    result = []
    botleft = true90bottom
    botright = true90bottom
    result.append(Move(LT, 5, 0.1))
    result.append(Move(RT, 175, 0.1))
    for j in range(5):
        for i in range(1, 4):
            result.append(Move(LB, botleft + 5 * i, 0.01))
            result.append(Move(RB, botright - 5 * i, 0.01))
        botleft += 15
        botright -= 15
        for i in range(1, 6):
            result.append(Move(LB, botleft - 5 * i, 0.05))
            result.append(Move(RB, botright + 5 * i, 0.05))
        botleft = true90bottom
        botright = true90bottom
        for i in range(1, 4):
            result.append(Move(LB, botleft + 5 * i, 0.01))
            result.append(Move(RB, botright - 5 * i, 0.01))
        botleft += 15
        botright -= 15
        for i in range(1, 6):
            result.append(Move(LB, botleft - 5 * i, 0.05))
            result.append(Move(RB, botright + 5 * i, 0.05))

    result.append(Move(LT, true90top, 0.5))
    result.append(Move(RT, true90top, 0.5))
    return result


# Move 6 as a list
humpingMove = humping()
humpingCopy = humping()

def skate_move():
    result = []
    righttop = true90top
    lefttop = true90top
    result.append(Move(LB, 150, 0.05))
    for i in range(1, 7):
        result.append(Move(LT, lefttop - 10 * i, 0.02))
    lefttop -= 60
    result.append(Move(LB, true90bottom, 0.05))
    for i in range(1, 7):
        result.append(Move(LT, lefttop + 10 * i, 0.02))
    lefttop = true90top
    result.append(Move(RB, 30, 0.05))
    for i in range(1, 7):
        result.append(Move(RT, righttop + 10 * i, 0.02))
    righttop += 60
    result.append(Move(RB, true90bottom, 0.05))
    for i in range(1, 7):
        result.append(Move(RT, righttop - 10 * i, 0.02))
    righttop = true90top
    return result

skate = skate_move()
skate_copy = skate_move()


french_song = []
french_song.extend(turnLeftCopy)
french_song.extend(skate_copy)
french_song.extend(Move1_copy)
french_song.extend(turnRightCopy)
french_song.extend(skate_copy)
french_song.extend(Move1_copy)

french_song_copy = []
french_song_copy.extend(turnLeftCopy)
french_song_copy.extend(skate_copy)
french_song_copy.extend(Move1_copy)
french_song_copy.extend(turnRightCopy)
french_song_copy.extend(skate_copy)
french_song_copy.extend(Move1_copy)


