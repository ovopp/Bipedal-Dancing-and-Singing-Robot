"""
WELCOME TO THE GROUP 20's DANCING, SINGING, SLIDING, BOUNCING ROBOT
======================================================================
Dance moves are in TryMoves.py, using a data-class, we're able to pull move
objects to move the servos
Buzzer and music are all written here, with a complex play function
Bluetooth functionality is also here
Images in bmp files are all in the itsy-bitsy

"""


import time
import board
import pulseio
import displayio
import terminalio
import TryMoves
import busio
from adafruit_st7735r import ST7735R
from TryMoves import Move

# Releases all previous displays
displayio.release_displays()

# LCD Initialization

spi = board.SPI()
tft_cs = board.A2
tft_dc = board.A4
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.A3)
display = ST7735R(display_bus, width=128, height=128, colstart=2, rowstart=1)

# Bluetooth UART
uart = busio.UART(board.TX, board.RX, baudrate=9600)

'''
Function that reads the bluetooth bluefruit input buffer, clears it, and then sets the bluetooth_input variable
'''


def readBluetooth():
    global bluetooth_input
    data = uart.read(8)
    print(data)
    data = str(data)
    if data is not None:
        # decodes the data if it's a valid input
        if len(data) == 11:
            # the 4th byte should contain the button value
            data = data[4]
            if data == "1":
                bluetooth_input = 1
            elif data == "2":
                bluetooth_input = 2
            elif data == "3":
                bluetooth_input = 3
            elif data == "4":
                bluetooth_input = 0
            else:
                bluetooth_input = 4  # idle state
    # clears the UART buffer
    while uart.read(32) is not None:
        pass
    print("Current Bluetooth input is: " + str(bluetooth_input))


# Calibrated Servo 90 degrees
true90top = 97
true90bottom = 87

# Index for dance moves
danceMoveIndex = 0

# speed for Careless Whisper
tempo = 3  # three seconds for each bar

# Define a dictionary of tones/music notes to play.
music_notes = {'C2': 131, 'A3': 220, 'Bb3': 233, 'B3': 247, 'C3': 262, 'Db3': 277, 'D3': 293, 'Eb3': 311, 'E3': 330,
               'F3': 349,
               'F#3': 370, 'G3': 392, 'G#3': 415,
               'A4': 440, 'Bb4': 466, 'B4': 494, 'C4': 523, 'D4': 587, 'E4': 659, 'F4': 698, 'G4': 784, 'G#4': 830,
               'Ab4': 415, 'C#4': 554, 'Eb4': 622, 'A5': 880, 'Ab5': 830, 'N': 0,
               'Bb5': 932, 'C5': 1046, 'nop': 50
               }

'''
input from bluetooth input
0 = careless whisper
1 = soviet
2 = solar
3 = french
else: idle state
'''

# initial bluetooth_input to idle state
bluetooth_input = 4

# Create piezo buzzer PWM output.
buzzer = pulseio.PWMOut(board.D5, variable_frequency=True)

# Start at the first note and start making sound.
buzzer.duty_cycle = 2 ** 15  # 32768 value is 50% duty cycle, a square wave.

'''
Driver for servo and buzzer play functionality
'''


def play(note, duration, buzz, movelist, movelistcopy):
    global danceMoveIndex
    if music_notes[note] == 0:
        buzz.duty_cycle = 0
        time.sleep(duration)
        buzz.duty_cycle = 2 ** 15

    else:
        '''
        Plays the note for the set duration,
        while the duration of the note is still happening, the servos will move
        based on the move list passed
        '''
        buzz.frequency = music_notes[note]
        t = time.monotonic()
        t2 = time.monotonic()
        # Checks to see if t2 (which gets updated after each servo move) - t1 is still less than duration of the note
        while t2 - t < 0.95 * duration:
            """
            take a move from the danceMoveList, and using the
            Move class from TryMoves.py to move servos
            """
            if danceMoveIndex < len(movelist):
                move = movelist[danceMoveIndex]
                move.limb.angle = move.degree
                if move.duration > duration - (t2 - t):
                    time.sleep(duration - t2 + t)
                    # if a move has not finished, it will rest for the remaining amount of time of the note, and
                    # change the danceMove list with a same move but with the remaining time
                    movelist[danceMoveIndex] = Move(move.limb, move.degree, move.duration - (duration - (t2 - t)))
                else:
                    time.sleep(move.duration)
                    danceMoveIndex += 1
            else:
                """
                Once the dance-move is run out, reset the danceMoveIndex
                so that the dance can start all over, and also the dance
                move list will be refreshed with a copy of the dance moves
                """
                danceMoveIndex = 0  # restarts the dance-move
                for i in range(len(movelist)):
                    movelist[i] = movelistcopy[i]
            t2 = time.monotonic()

        buzz.duty_cycle = 0
        time.sleep(duration * 0.05)
        buzz.duty_cycle = 2 ** 15


'''
List of play functions
with various tempo timings
'''


def restQuarter(buzz):
    buzz.duty_cycle = 0
    time.sleep(tempo / 4)
    buzzer.duty_cycle = 2 ** 15


def restEigth(buzz):
    buzz.duty_cycle = 0
    time.sleep(tempo / 8)
    buzzer.duty_cycle = 2 ** 15


def play16th(note, buzz):
    play(note, tempo / 16, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def play8th(note, buzz):
    play(note, tempo / 8, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playDot8th(note, buzz):
    play(note, tempo / 8 + tempo / 16, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playQuarter(note, buzz):
    play(note, tempo / 4, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playDotQuarter(note, buzz):
    play(note, tempo / 4 + tempo / 8, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playHalf(note, buzz):
    play(note, tempo / 2, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playQuarterand16th(note, buzz):
    play(note, tempo / 4 + tempo / 16, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playHalfand16th(note, buzz):
    play(note, tempo / 2 + tempo / 16, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playHalfand8th(note, buzz):
    play(note, tempo / 2 + tempo / 8, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def play25(note, buzz):
    play(note, tempo * 0.625, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def play3(note, buzz):
    play(note, tempo * 0.75, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playWhole(note, buzz):
    play(note, tempo, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


def playWhole8(note, buzz):
    play(note, tempo + tempo / 8, buzz, TryMoves.humpingMove, TryMoves.humpingCopy)


'''
Songs by Jason (Solar and Careless Whisper)
'''


def Solar():
    global tempo
    tempo = 1.2

    for i in range(len(SolarFunctions)):
        SolarFunctions[i](*SolarNotes[i])


# Careless Whisper
# https://www.musicnotes.com/images/productimages/large/mtd/MN0114022.gif
def CarelessWhisper():
    global tempo
    tempo = 3

    for i in range(len(WhisperFunctions)):
        WhisperFunctions[i](*WhisperNotes[i])


SolarFunctions = [restEigth, playDotQuarter, play8th, play8th, play3, restEigth, play8th,
                  playQuarter, playQuarter, playQuarter, play8th, playWhole8,
                  playDotQuarter, restEigth, playQuarter, play8th, play8th,
                  play25, restEigth, play8th, play8th,
                  play8th, playQuarter, playQuarter, playQuarter, play8th, playHalfand8th, restQuarter, restEigth,

                  playDotQuarter, play8th, play8th, play8th, playQuarter,
                  playDotQuarter, play8th, play8th, play8th, playQuarter,

                  playWhole8,
                  restEigth, play8th, play8th, play8th, play8th, play8th, playQuarter]
SolarNotes = [(buzzer,), ('C4', buzzer), ('B4', buzzer), ('D4', buzzer), ('C4', buzzer), (buzzer,), ('G3', buzzer),
              ('A4', buzzer), ('Bb4', buzzer), ('Bb4', buzzer), ('A4', buzzer), ('C4', buzzer),
              ('Bb4', buzzer), (buzzer,), ('A4', buzzer), ('G#3', buzzer), ('Bb4', buzzer),
              ('A4', buzzer), (buzzer,), ('C3', buzzer), ('F3', buzzer),
              ('G3', buzzer), ('G#3', buzzer), ('G#3', buzzer), ('G3', buzzer), ('Bb4', buzzer), ('G#3', buzzer),
              (buzzer,), (buzzer,),

              ('G3', buzzer), ('F3', buzzer), ('Eb3', buzzer), ('D3', buzzer), ('C3', buzzer),
              ('F#3', buzzer), ('F3', buzzer), ('Eb3', buzzer), ('Db3', buzzer), ('C3', buzzer),
              ('F3', buzzer),
              (buzzer,), ('D3', buzzer), ('Eb3', buzzer), ('F3', buzzer), ('G3', buzzer), ('G#3', buzzer),
              ('B4', buzzer)]

WhisperFunctions = [play8th, play8th, play16th, playDot8th, play8th, play8th, play16th, playDot8th, play8th,
                    play8th, play16th, playDot8th, play8th, play8th, play16th, playDot8th, play8th,
                    play8th, play16th, playDot8th, play8th, playHalf,
                    play8th, play8th, play8th, play8th, play8th, play8th, play8th, play8th,
                    play8th, playQuarter, playQuarter, playQuarter, playDotQuarter, restQuarter, restQuarter, play8th,
                    play16th, play16th,
                    playQuarter, play8th, playDot8th, play8th, play8th, play8th,
                    playQuarter, playQuarter, playQuarter, playQuarter,
                    restEigth, play16th, play16th, play8th, play16th, playHalfand16th,
                    restEigth, play16th, play16th, play8th, play16th, playDot8th, playDotQuarter,
                    play8th, play8th, play8th, play8th, play8th, play16th, playQuarterand16th,
                    playQuarter, playQuarter, playQuarter, playDot8th, play16th,
                    restEigth, play8th, play16th, play16th, play16th, play16th, play8th, play16th, playQuarterand16th,
                    play8th, play8th, play16th, playDot8th, play8th, play8th, play8th, play8th,
                    restEigth, play16th, play16th, play8th, play8th, play8th, play16th, playQuarterand16th,
                    play8th, play16th, play16th, playDot8th, play16th, playDot8th, playQuarterand16th,
                    play16th, play16th, play8th, play8th, play16th, play16th, play8th, play16th, playQuarterand16th,
                    play8th, play8th, play16th, playDot8th, playDot8th, play16th, play8th, play8th,
                    restEigth, play16th, play16th, play16th, play16th, play16th, play16th, play8th, play16th, play8th,
                    play16th,
                    playDot8th, play16th, play16th, playDot8th, playQuarter, playQuarter,
                    playHalf, restQuarter, restEigth, play8th,
                    playHalf, playQuarter, restQuarter,
                    playQuarter, play8th, playQuarter, playQuarter, play8th,
                    play8th, playQuarter, playHalf, play8th,
                    play8th, play16th, playDot8th, play8th, play8th, play16th, playDot8th, play8th,
                    play8th, play16th, playDot8th, play8th, play8th, play16th, playDot8th, play8th,
                    play8th, play16th, playDot8th, play8th, playHalf,
                    play8th, play8th, play8th, play8th, play8th, play8th, play8th, play8th,
                    play8th, play16th, playDot8th, play8th, play8th, play16th, playDot8th, play8th,
                    play8th, play16th, playDot8th, play8th, play8th, play16th, playDot8th, play8th,
                    play8th, play16th, playDot8th, play8th, playHalf,
                    play8th, play8th, play8th, play8th, play8th, play8th, play8th, play8th]

WhisperNotes = [('F3', buzzer), ('E4', buzzer), ('D4', buzzer), ('A4', buzzer), ('F3', buzzer), ('E4', buzzer),
                ('D4', buzzer), ('A4', buzzer), ('F3', buzzer),
                ('C4', buzzer), ('Bb4', buzzer), ('F3', buzzer), ('D3', buzzer), ('C4', buzzer), ('Bb4', buzzer),
                ('F3', buzzer), ('D3', buzzer),
                ('Bb4', buzzer), ('A4', buzzer), ('F3', buzzer), ('D3', buzzer), ('Bb3', buzzer),
                ('A3', buzzer), ('Bb3', buzzer), ('C3', buzzer), ('D3', buzzer), ('E3', buzzer), ('F3', buzzer),
                ('G3', buzzer), ('A4', buzzer),
                ('A4', buzzer), ('A4', buzzer), ('G3', buzzer), ('F3', buzzer), ('D3', buzzer), (buzzer,), (buzzer,),
                ('C3', buzzer), ('D3', buzzer), ('D3', buzzer),
                ('A4', buzzer), ('Bb4', buzzer), ('G3', buzzer), ('D3', buzzer), ('F3', buzzer), ('D3', buzzer),
                ('A4', buzzer), ('G3', buzzer), ('F3', buzzer), ('E3', buzzer),
                (buzzer,), ('D3', buzzer), ('E3', buzzer), ('F3', buzzer), ('G3', buzzer), ('A4', buzzer),
                (buzzer,), ('D3', buzzer), ('E3', buzzer), ('F3', buzzer), ('D3', buzzer), ('C4', buzzer),
                ('Bb4', buzzer),
                ('A4', buzzer), ('Bb4', buzzer), ('A4', buzzer), ('Bb4', buzzer), ('A4', buzzer), ('Bb4', buzzer),
                ('A4', buzzer),
                ('A4', buzzer), ('G3', buzzer), ('F3', buzzer), ('E3', buzzer), ('D3', buzzer),
                (buzzer,), ('F4', buzzer), ('F4', buzzer), ('E4', buzzer), ('E4', buzzer), ('E4', buzzer),
                ('E4', buzzer), ('D4', buzzer), ('D4', buzzer),
                ('F4', buzzer), ('D4', buzzer), ('F4', buzzer), ('D4', buzzer), ('G4', buzzer), ('F4', buzzer),
                ('E4', buzzer), ('D4', buzzer),
                (buzzer,), ('F4', buzzer), ('F4', buzzer), ('F4', buzzer), ('E4', buzzer), ('E4', buzzer),
                ('D4', buzzer), ('D4', buzzer),
                ('D4', buzzer), ('E4', buzzer), ('E4', buzzer), ('E4', buzzer), ('C4', buzzer), ('D4', buzzer),
                ('C4', buzzer),
                ('F4', buzzer), ('F4', buzzer), ('F4', buzzer), ('F4', buzzer), ('E4', buzzer), ('E4', buzzer),
                ('E4', buzzer), ('D4', buzzer), ('D4', buzzer),
                ('F4', buzzer), ('D4', buzzer), ('F4', buzzer), ('D4', buzzer), ('G4', buzzer), ('F4', buzzer),
                ('E4', buzzer), ('D4', buzzer),
                (buzzer,), ('F4', buzzer), ('F4', buzzer), ('F4', buzzer), ('E4', buzzer), ('E4', buzzer),
                ('E4', buzzer), ('E4', buzzer), ('D4', buzzer), ('D4', buzzer), ('D4', buzzer),
                ('E4', buzzer), ('E4', buzzer), ('D4', buzzer), ('E4', buzzer), ('F4', buzzer), ('E4', buzzer),
                ('D4', buzzer), (buzzer,), (buzzer,), ('C4', buzzer),
                ('C4', buzzer), ('Bb4', buzzer), (buzzer,),
                ('E3', buzzer), ('F3', buzzer), ('G3', buzzer), ('A4', buzzer), ('A4', buzzer),
                ('E4', buzzer), ('F4', buzzer), ('D4', buzzer), ('F3', buzzer),
                ('E4', buzzer), ('D4', buzzer), ('A4', buzzer), ('F3', buzzer), ('E4', buzzer), ('D4', buzzer),
                ('A4', buzzer), ('F3', buzzer),
                ('C4', buzzer), ('Bb4', buzzer), ('F3', buzzer), ('D3', buzzer), ('C4', buzzer), ('Bb4', buzzer),
                ('F3', buzzer), ('D3', buzzer),
                ('Bb4', buzzer), ('A4', buzzer), ('F3', buzzer), ('D3', buzzer), ('Bb3', buzzer),
                ('A3', buzzer), ('Bb3', buzzer), ('C3', buzzer), ('D3', buzzer), ('E3', buzzer), ('F3', buzzer),
                ('G3', buzzer), ('A4', buzzer),
                ('E4', buzzer), ('D4', buzzer), ('A4', buzzer), ('F3', buzzer), ('E4', buzzer), ('D4', buzzer),
                ('A4', buzzer), ('F3', buzzer),
                ('C4', buzzer), ('Bb4', buzzer), ('F3', buzzer), ('D3', buzzer), ('C4', buzzer), ('Bb4', buzzer),
                ('F3', buzzer), ('D3', buzzer),
                ('Bb4', buzzer), ('A4', buzzer), ('F3', buzzer), ('D3', buzzer), ('Bb3', buzzer),
                ('A3', buzzer), ('Bb3', buzzer), ('C3', buzzer), ('D3', buzzer), ('E3', buzzer), ('F3', buzzer),
                ('G3', buzzer), ('A4', buzzer)]

'''
Songs by Andrew: To The Tsar and French Song
'''


def toTheTsar(s):
    notes = [('C4', 6 * s), ('N', 2 * s), ('G3', 2 * s),
             ('C4', 4 * s), ('G3', 3 * s), ('A4', 1 * s), ('B4', 4 * s), ('E3', 2 * s), ('E3', 2 * s), ('A4', 4 * s),
             ('G3', 3 * s), ('F3', 1 * s), ('G3', 4 * s), ('C3', 2 * s), ('C3', 2 * s), ('D3', 4 * s), ('D3', 2 * s),
             ('E3', 2 * s), ('F3', 4 * s), ('F3', 2 * s), ('G3', 2 * s),
             ('A4', 4 * s), ('B4', 2 * s), ('C4', 2 * s), ('D4', 4 * s), ('N', 2 * s), ('G3', 2 * s), ('E4', 4 * s),
             ('D4', 3 * s), ('C4', 1 * s), ('D4', 4 * s), ('B4', 2 * s), ('G3', 2 * s), ('C4', 4 * s), ('B4', 3 * s),
             ('A4', 1 * s), ('B4', 4 * s), ('E3', 2 * s), ('E3', 2 * s), ('A4', 4 * s), ('G3', 2 * s), ('F3', 2 * s),
             ('G3', 4 * s), ('C3', 2 * s), ('C3', 2 * s), ('C4', 4 * s), ('B4', 3 * s), ('A4', 1 * s), ('G3', 6 * s),
             ('N', 2 * s),
             ('E4', 8 * s), ('D4', 2 * s), ('C4', 2 * s), ('B4', 2 * s), ('C4', 2 * s), ('D4', 6 * s), ('G3', 2 * s),
             ('G3', 8 * s), ('C4', 8 * s), ('B4', 2 * s), ('A4', 2 * s), ('G3', 2 * s), ('A4', 2 * s), ('B4', 6 * s),
             ('E4', 2 * s), ('E4', 6 * s), ('N', 2 * s), ('C4', 4 * s), ('A4', 3 * s), ('B4', 1 * s), ('C4', 4 * s),
             ('A4', 3 * s), ('B4', 1 * s),
             ('C4', 4 * s), ('A4', 3 * s), ('C4', 1 * s), ('F4', 6 * s), ('N', 2 * s), ('F4', 8 * s), ('E4', 2 * s),
             ('D4', 2 * s), ('C4', 2 * s), ('D4', 2 * s), ('E4', 6 * s), ('C4', 2 * s), ('C4', 8 * s), ('D4', 8 * s),
             ('C4', 2 * s), ('B4', 2 * s), ('A4', 2 * s), ('B4', 2 * s), ('C4', 6 * s), ('A4', 2 * s), ('A4', 6 * s),
             ('N', 2 * s),
             ('C4', 4 * s), ('B4', 2 * s), ('A4', 2 * s), ('G3', 4 * s), ('C3', 2 * s), ('N', 1 * s), ('C3', 2 * s),
             ('G3', 8 * s), ('A4', 4 * s), ('B4', 4 * s), ('C4', 20 * s)]
    for t in notes:
        play(t[0], t[1], buzzer, TryMoves.dab, TryMoves.dab_copy)


def frenchSong(s):
    notes = [
        ['E3', 2], ['A4', 2], ['B4', 2], ['C4', 2], ['B4', 4], ['A4', 2], ['E3', 6],
        ['N', 2], ['E3', 2], ['A4', 2], ['B4', 2], ['C4', 2], ['E4', 4],
        ['G4', 4], ['F4', 2], ['B4', 10],
        ['N', 10], ['B4', 2], ['C4', 2], ['D4', 4],
        ['C#4', 2], ['D4', 2], ['E4', 4], ['D4', 2], ['E4', 2], ['F4', 8],
        ['N', 2], ['E4', 2], ['D4', 2], ['C4', 2], ['B4', 2],
        ['B4', 4], ['A4', 2], ['C3', 10],
        ['N', 16], ['E3', 2], ['A4', 2], ['B4', 2], ['C4', 2], ['B4', 4], ['A4', 2], ['E3', 6],
        ['N', 2], ['E3', 2], ['A4', 2], ['B4', 2], ['C4', 2], ['E4', 4],
        ['G4', 4], ['F4', 2], ['B4', 10],
        ['N', 10], ['B4', 2], ['C4', 2], ['D4', 4],
        ['C#4', 2], ['D4', 2], ['E4', 4], ['D4', 2], ['E4', 2], ['F4', 8],
        ['N', 2], ['E4', 2], ['D4', 2], ['C4', 2], ['B4', 2],
        ['B4', 4], ['C4', 2], ['G3', 10],
        ['N', 6], ['G3', 2], ['D4', 4], ['C4', 4],
        ['B4', 4], ['A4', 2], ['G#3', 10],
        ['N', 16], ['E3', 2], ['A4', 2], ['B4', 2], ['C4', 2], ['B4', 4], ['A4', 2], ['E3', 6],
        ['N', 2], ['E3', 2], ['A4', 2], ['B4', 2], ['C4', 2], ['E4', 2],
        ['G4', 4], ['F4', 2], ['B4', 10],
        ['N', 10], ['B4', 2], ['C4', 2], ['D4', 4],
        ['C#4', 2], ['D4', 2], ['E4', 4], ['D4', 2], ['E4', 2], ['F4', 8],
        ['N', 2], ['E4', 2], ['D4', 2], ['C4', 2], ['B4', 2],
        ['B4', 4], ['A4', 2], ['C4', 10],
        ['N', 16],
        ['E3', 2], ['A4', 2], ['B4', 2], ['C4', 2], ['B4', 4], ['A4', 2], ['E3', 6],
        ['N', 2], ['E3', 2], ['A4', 2], ['B4', 2], ['C4', 2], ['E4', 2],
        ['G4', 4], ['F4', 2], ['B4', 10],
        ['N', 10], ['B4', 2], ['C4', 2], ['D4', 4],
        ['C#4', 2], ['D4', 2], ['E4', 4], ['D4', 2], ['E4', 2], ['F4', 8],
        ['N', 2], ['E4', 2], ['D4', 2], ['C4', 2], ['B4', 2],
        ['B4', 4], ['C4', 2], ['G3', 10],
        ['N', 6], ['G3', 2], ['D4', 4], ['C4', 4],
        ['B4', 4], ['A4', 2], ['G#3', 10],
        ['N', 16],
        ['E3', 1], ['A4', 1], ['B4', 1], ['N', 5], ['E3', 1], ['A4', 1], ['D4', 1], ['N', 5],
        ['E3', 1], ['A4', 1], ['B4', 1], ['N', 1], ['E3', 1], ['A4', 1], ['B4', 1], ['N', 1], ['E3', 1], ['A4', 1],
        ['D4', 1], ['N', 5],
        ['F3', 1], ['A4', 1], ['B4', 1], ['N', 5], ['F3', 1], ['A4', 1], ['D4', 1], ['N', 5],
        ['F3', 1], ['A4', 1], ['B4', 1], ['N', 1], ['F3', 1], ['A4', 1], ['B4', 1], ['N', 1], ['F3', 1], ['A4', 1],
        ['D4', 1], ['N', 5],
        ['E3', 1], ['A4', 1], ['B4', 1], ['N', 5], ['E3', 1], ['A4', 1], ['D4', 1], ['N', 5],
        ['E3', 1], ['A4', 1], ['B4', 1], ['N', 1], ['E3', 1], ['A4', 1], ['B4', 1], ['N', 1], ['E3', 1], ['A4', 1],
        ['D4', 1], ['N', 5],
        ['F3', 1], ['A4', 1], ['B4', 1], ['N', 5], ['F3', 1], ['A4', 1], ['D4', 1], ['N', 5],
        ['F3', 1], ['A4', 1], ['B4', 1], ['N', 1], ['F3', 1], ['A4', 1], ['B4', 1], ['N', 1], ['F3', 1], ['A4', 1],
        ['D4', 1], ['N', 5], ['G3', 2], ['C4', 2], ['D4', 2], ['Eb4', 2], ['D4', 4], ['C4', 2], ['G3', 4],
        ['N', 2], ['G3', 2], ['C4', 2], ['D4', 2], ['Eb4', 2], ['G4', 2],
        ['Bb5', 4], ['Ab4', 2], ['D4', 10],
        ['N', 10], ['D4', 2], ['Eb4', 2], ['F4', 4],
        ['E4', 2], ['F4', 2], ['G4', 4], ['F4', 2], ['G4', 2], ['Ab5', 8],
        ['N', 2], ['G4', 2], ['F4', 2], ['Eb4', 2], ['D4', 2],
        ['D4', 4], ['C4', 2], ['Eb4', 10],
        ['N', 10],
        ['G3', 2], ['C4', 2], ['D4', 2], ['Eb4', 2], ['D4', 4], ['C4', 2], ['G3', 4],
        ['N', 2], ['G3', 2], ['C4', 2], ['D4', 2], ['Eb4', 2], ['G4', 2],
        ['Bb5', 4], ['Ab4', 2], ['D4', 10],
        ['N', 10], ['D4', 2], ['Eb4', 2], ['F4', 4],
        ['E4', 2], ['F4', 2], ['G4', 4], ['F4', 2], ['G4', 2], ['Ab5', 8],
        ['N', 2], ['G4', 2], ['F4', 2], ['Eb4', 2], ['D4', 2], ['D4', 4], ['Eb4', 2], ['Bb4', 10],
        ['N', 6], ['Bb4', 2], ['F4', 4], ['Eb4', 4],
        ['D4', 4], ['C2', 2], ['B4', 10],
        ['N', 16],
        ['G3', 1], ['C4', 1], ['D4', 1], ['N', 5], ['G3', 1], ['C4', 1], ['F4', 1], ['N', 5],
        ['G3', 1], ['C4', 1], ['D4', 1], ['N', 1], ['G3', 1], ['C4', 1], ['D4', 1], ['N', 1], ['G3', 1], ['C4', 1],
        ['F4', 1], ['N', 5],
        ['Ab4', 1], ['C4', 1], ['D4', 1], ['N', 5], ['Ab4', 1], ['C4', 1], ['F4', 1], ['N', 5],
        ['Ab4', 1], ['C4', 1], ['D4', 1], ['N', 1], ['Ab4', 1], ['C4', 1], ['D4', 1], ['N', 1], ['Ab4', 1],
        ['C4', 1], ['F4', 1], ['N', 5],
        ['G3', 2], ['C4', 2], ['D4', 2], ['Eb4', 2], ['D4', 4], ['C4', 2], ['G3', 6],
        ['N', 2], ['G3', 2], ['C4', 2], ['D4', 2], ['Eb4', 2], ['G4', 2],
        ['Bb5', 4], ['Ab5', 2], ['D4', 10],
        ['N', 10], ['D4', 2], ['Eb4', 2], ['F4', 4],
        ['E4', 2], ['F4', 2], ['G4', 4], ['F4', 2], ['G4', 2], ['Ab5', 8],
        ['N', 2], ['G4', 2], ['F4', 2], ['Eb4', 2], ['D4', 2],
        ['D4', 4], ['C4', 2], ['Eb4', 10],
        ['N', 16],
        ['G3', 2], ['C4', 2], ['D4', 2], ['Eb4', 2], ['D4', 4], ['C4', 2], ['G3', 6],
        ['N', 2], ['G3', 2], ['C4', 2], ['D4', 2], ['Eb4', 2], ['G4', 2],
        ['Bb5', 4], ['Ab5', 2], ['D4', 10],
        ['N', 10], ['D4', 2], ['Eb4', 2], ['F4', 4],
        ['E4', 2], ['F4', 2], ['G4', 4], ['F4', 2], ['G4', 2], ['Ab5', 8],
        ['N', 2], ['G4', 2], ['F4', 2], ['Eb4', 2], ['D4', 2],
        ['D4', 4], ['C4', 2], ['Eb4', 10]
    ]
    for t in notes:
        play(t[0], t[1] * s, buzzer, TryMoves.french_song, TryMoves.french_song_copy)


'''
Routines based on the bluetooth_input
Routines will display a photo, followed by a while loop that checks the input of the bluetooth_input and plays the
correct song with the corresponding dance.
Once a song is finished, the a bluetooth reading will commence, and if changed, will exit and
continue back to the main while loop
'''


def CarelessRoutine():
    with open("/careless.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)

        while bluetooth_input == 0:
            TryMoves.resetServo()
            CarelessWhisper()
            buzzer.duty_cycle = 0
            readBluetooth()
            buzzer.duty_cycle = 2**15


def FrenchRoutine():
    with open("/french song.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)

        while bluetooth_input == 3:
            TryMoves.resetServo()
            frenchSong(0.1)
            buzzer.duty_cycle = 0
            readBluetooth()
            buzzer.duty_cycle = 2**15


def SolarRoutine():
    with open("/solar.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)

        while bluetooth_input == 2:
            TryMoves.resetServo()
            Solar()
            buzzer.duty_cycle = 0
            readBluetooth()
            buzzer.duty_cycle = 2**15


def SovietRoutine():
    with open("/soviet.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)

        while bluetooth_input == 1:
            TryMoves.resetServo()
            toTheTsar(0.2)
            buzzer.duty_cycle = 0
            readBluetooth()
            buzzer.duty_cycle = 2 ** 15


'''
Default Routine when the robot is started.
Also when a button that is not 1-4 is not pressed on the keypad
After each move, the robot will check with the bluefruit, to make sure
if there's an input, the robot will break and start the new routine
'''


def IdleRoutine():

    with open("/skate.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)
        for j in range(5):
            for i in range(len(TryMoves.skate_copy)):
                move = TryMoves.skate_copy[i]
                move.limb.angle = move.degree
                time.sleep(move.duration)
        readBluetooth()

    if bluetooth_input is not 4:
        return

    with open("/lkick.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)
        TryMoves.resetServo()
        for j in range(3):
            for i in range(len(TryMoves.Move1_copy)):
                move = TryMoves.Move1_copy[i]
                move.limb.angle = move.degree
                time.sleep(move.duration)
        readBluetooth()

    if bluetooth_input is not 4:
        return

    with open("/wave.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)
        TryMoves.resetServo()
        for j in range(5):
            for i in range(len(TryMoves.wave_copy)):
                move = TryMoves.wave_copy[i]
                move.limb.angle = move.degree
                time.sleep(move.duration)
        readBluetooth()

    if bluetooth_input is not 4:
        return

    with open("/dab.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)
        TryMoves.resetServo()
        for j in range(5):
            for i in range(len(TryMoves.dab_copy)):
                move = TryMoves.dab_copy[i]
                move.limb.angle = move.degree
                time.sleep(move.duration)
        readBluetooth()

    if bluetooth_input is not 4:
        return

    with open("/left.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)
        TryMoves.resetServo()
        for j in range(5):
            for i in range(len(TryMoves.turnLeftCopy)):
                move = TryMoves.turnLeftCopy[i]
                move.limb.angle = move.degree
                time.sleep(move.duration)
        readBluetooth()

    if bluetooth_input is not 4:
        return

    with open("/humping.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)
        TryMoves.resetServo()
        for j in range(3):
            for i in range(len(TryMoves.humpingCopy)):
                move = TryMoves.humpingCopy[i]
                move.limb.angle = move.degree
                time.sleep(move.duration)
        readBluetooth()

    if bluetooth_input is not 4:
        return

    with open("/right.bmp", "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)

        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

        # Create a Group to hold the TileGrid
        group = displayio.Group()

        # Add the TileGrid to the Group
        group.append(tile_grid)

        # Add the Group to the Display
        display.show(group)
        TryMoves.resetServo()
        for j in range(5):
            for i in range(len(TryMoves.turnRightCopy)):
                move = TryMoves.turnRightCopy[i]
                move.limb.angle = move.degree
                time.sleep(move.duration)
        TryMoves.resetServo()
        readBluetooth()


'''
Main function just consists of a while loop
This while loop will check the value of bluetooth_input to make sure
to go to the correct routine.
'''

while True:
    if bluetooth_input == 0:
        buzzer.duty_cycle = 2**15
        CarelessRoutine()
        buzzer.duty_cycle = 0
    elif bluetooth_input == 1:
        buzzer.duty_cycle = 2**15
        SovietRoutine()
        buzzer.duty_cycle = 0
    elif bluetooth_input == 2:
        buzzer.duty_cycle = 2**15
        SolarRoutine()
        buzzer.duty_cycle = 0
    elif bluetooth_input == 3:
        buzzer.duty_cycle = 2**15
        FrenchRoutine()
        buzzer.duty_cycle = 0
    else:
        buzzer.duty_cycle = 0
        TryMoves.resetServo()
        IdleRoutine()
