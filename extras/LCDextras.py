import Adafruit_CharLCDPlate
from time import sleep

def clearRight(lcd):
	j = 0
	while(j < 16):
		lcd.scrollDisplayRight()
		sleep(.04)
		j += 1

def clearLeft(lcd):
	i = 0
	while(i < 16):
		lcd.scrollDisplayLeft()
		sleep(.04)
		i += 1

def enterRight(lcd):
#	for n in range(16):
#		lcd.scrollDisplayLeft()
	for s in range(16):
		lcd.scrollDisplayRight()
		sleep(.04)

def enterLeft(lcd):
 #       for n in range(16):
#                lcd.scrollDisplayRight()
        for s in range(16):
                lcd.scrollDisplayLeft()
                sleep(.04)
