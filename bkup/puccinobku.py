import os
import atexit
import ConfigParser
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

plugins = []
current_index = 0
lcd = Adafruit_CharLCDPlate()
config = ConfigParser.ConfigParser()
config.read('settings.ini')

def exit_handler():
    lcd.clear()
    lcd.backlight(lcd.OFF)
    print("PiPuccino has lost its steam...")
atexit.register(exit_handler)

plugin_list = ""
for p in os.listdir('plugins'):
    if p.endswith('.py'):
        plugins.append(p)
        plugin_list+= str(p) + ' '

print("Loaded plugins: " + plugin_list)

#Run plugin based on current index of the list
#Wait for exit_handler of plugin to finish
while True:
    try:
        if current_index == len(plugins):
            current_index = 0
        c_plugin = plugins[current_index][:-3]

        if current_index == len(plugins)-1:
            n_plugin = plugins[0][:-3]
        else: n_plugin = plugins[current_index+1][:-3]

        execfile('plugins/' + plugins[current_index])

        #After exit handler from plugin finishes, switch plugin
        lcd.clear()
        lcd.backlight(lcd.TEAL)
        current_index += 1
        print("Plugin switch: %s ---> %s" % (c_plugin, n_plugin))
    except KeyboardInterrupt:
        exit()