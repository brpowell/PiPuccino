import sys
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

lcd = Adafruit_CharLCDPlate()
lcd.backlight(lcd.ON)

power = True

print("\nLCD console\nType 'help' for available commands")

while True:
	try:
		command = raw_input(">>> ").split()
		
		if command[0] == 'backlight':
			if command[1] == 'toggle':	
				if power: lcd.backlight(lcd.OFF); power = False
				else: lcd.backlight(lcd.ON); power = True
			elif command[1] == 'red': lcd.backlight(lcd.RED)
			elif command[1] == 'yellow': lcd.backlight(lcd.YELLOW)
			elif command[1] == 'green': lcd.backlight(lcd.GREEN)
			elif command[1] == 'teal': lcd.backlight(lcd.TEAL)
			elif command[1] == 'blue': lcd.backlight(lcd.BLUE)
			elif command[1] == 'violet': lcd.backlight(lcd.VIOLET)
			elif command[1] == 'white': lcd.backlight(lcd.WHITE)
			else:
				print("usage: backlight toggle; [color]")
		elif command[0] == 'print':
			message = ""
			for t in range(1, len(command)):
				message += command[t] + ' '
			lcd.message(message)
		elif command[0] == 'clear':
			lcd.clear()
		elif command[0] == 'quit':
			sys.exit()
		elif command[0] == 'help':
			print("\n----------------------------")
			print("backlight: toggle; [color]")
			print("print: [message]")
			print("clear")
			print("quit")
			print("----------------------------\n")
		else:
			print("Command not found")
	except IndexError:
		print("invalid command")
