# -*- coding: utf-8 -*-
import os
import logging
import argparse
import atexit
import ConfigParser
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from random import shuffle
from time import sleep


def exit_handler():
    lcd.clear()
    lcd.backlight(lcd.OFF)
    print("PiPuccino has lost its steam...")


#Initialize LCD and load settings
plugins = []
current_index = 0
lcd = Adafruit_CharLCDPlate()
config = ConfigParser.ConfigParser()
config.read('settings.ini')
atexit.register(exit_handler)
logging.basicConfig(filename='puccino.log', level=logging.DEBUG)

plugin_list = ""
for p in os.listdir('plugins/'):
    if p.endswith('.py'):
        plugins.append(p)
        plugin_list += str(p) + ' '
print("Loaded plugins: " + plugin_list)


#Argument parsing
parser = argparse.ArgumentParser(prog="PiPuccino")
parser.add_argument('-r', '--run', help="Run specific plugin first in the list")
args = parser.parse_args()
if args.run is not None:
    try:
        current_index = plugins.index(args.run+'.py')
        print("Starting " + args.run)
    except ValueError:
        print("No plugin named " + args.run + ". Starting plugin 0...")
        current_index = 0


#Scrolling variables for ticker
BLANK = "               "
start = 0
end = 15
speed = 0.15

lcd.backlight(lcd.VIOLET)
lang = ['hello', 'hola', 'konnichiwa', 'bonjour', 'ciao', 'annyeong haseyo', 'hallo', 'ni hao', 'as-salam alaykom', 'bok', 'hej', 'xin chao']
shuffle(lang)
welcome_message = BLANK + lang[0]

while start < len(welcome_message)+3:
    lcd.clear()
    lcd.message("   PiPuccino   \n"+welcome_message[start:end])
    start += 1; end += 1
    sleep(speed)
lcd.clear()

# Main Loop
# Run plugin based on current index of the list
# Wait for plugin to finish running then switch
while True:
    try:
        if current_index == len(plugins):
            current_index = 0

        c_plugin = plugins[current_index][:-3]
        if current_index == len(plugins)-1:
            n_plugin = plugins[0][:-3]
        else:
            n_plugin = plugins[current_index+1][:-3]

        execfile('plugins/' + plugins[current_index])

        lcd.clear()
        current_index += 1
        print("%s ---> %s" % (c_plugin, n_plugin))
    except KeyboardInterrupt:
        exit()
