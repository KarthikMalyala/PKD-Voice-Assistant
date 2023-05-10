#!/usr/bin/python
import math, time, serial

def get_command(channel, target):
        target = target * 4
        serialBytes = chr(0x84)+chr(channel)+chr(target & 0x7F)+chr((target >> 7) & 0x7F)
        return serialBytes

def oscillate(i, upper, lower, frequency):
    amplitude = (upper - lower) / 2
    offset = lower + amplitude
    frequency = frequency
    return amplitude * math.sin(2 * math.pi * frequency * i) + offset

exp = serial.Serial('/dev/ttyACM2')
ser = serial.Serial('/dev/ttyACM0')
ser.write(chr(0xAA))
ser.flush()

i=0

### HEAD #####
# DOWN_UP = 704, 2352
headDown = 704
headUp = 1800
yaw_normal = 1800
def head_up():
	ser.write(get_command(12,int(headUp)))
	ser.write(get_command(0, int(yaw_normal)))

def head_down():
	ser.write(get_command(12,int(headDown)))

### JAW ####
# OPEN_CLOSE = 1504, 976
jawOpen = 1500
jawClose = 1000
def speak():
	exp.write(get_command(0, int(jawOpen)))

def normal():
	exp.write(get_command(0, int(jawClose)))


#### PITCH #####
# LEFT_RIGHT (1) = 2352, 704
pitchLeft = 2300
pitchRight = 704
frequency = 0.00035

#### BLINK #####
# UPPER_CLOSE_OPEN (17) = 704, 1696
# LOWER_CLOSE_OPEN (11) = 2256, 1248 
upperLidOpen = 1200
upperLidClose = 900
lowerLidOpen = 1600
lowerLidClose = 1900

def blink():
	ser.write(get_command(17,int(upperLidClose)))
	ser.write(get_command(11,int(lowerLidClose)))
	time.sleep(0.2)
	ser.write(get_command(17,int(upperLidOpen)))
	ser.write(get_command(11,int(lowerLidOpen)))
	time.sleep(0.2)

#### SMILE #####
# R_MAX_MIN (20) = 2352, 1408
# L_MAX_MIN (4) = 1536, 704
smile_max_r = 2000
smile_max_l = 1500
smile_min_r = 1410
smile_min_l = 1200
jaw_down = 1200
jaw_up = 1000
def smile():
	exp.write(get_command(20,int(smile_max_r)))
	exp.write(get_command(4,int(smile_min_l)))
	exp.write(get_command(0,int(jaw_down)))
	time.sleep(0.02)
def noSmile():
	exp.write(get_command(20,int(smile_min_r)))
	exp.write(get_command(4,int(smile_max_l)))
	exp.write(get_command(0,int(jaw_up)))
	time.sleep(0.02)

while(True):
	# Disable Cheek Puff
	exp.write(get_command(3,int(2304)))
	i = i + 10
	print(i)
	if(i % 5000 == 0):
		print(oscillate(i, pitchLeft, pitchRight, frequency))
		ser.write(get_command(1,int(oscillate(i, pitchLeft, pitchRight, frequency))))

	#smile()
	time.sleep(0.01)
	if(i % 2500 == 0):
		blink()
		head_up()
		normal()


#ser.write(get_command(11,int(-25)))
#ser.write(get_command(17,int(25)))
#ser.write(get_command(0,0))

ser.close()
