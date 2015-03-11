import pywapi
#import urllib2
from time import sleep
from datetime import datetime
from multiprocessing import Process

def load_screen():
    while True:
        lcd.message("Yahoo!    [*   ]\n    Weather"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [ *  ]\n    Weather"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [  * ]\n    Weather"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [   *]\n    Weather"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [  * ]\n    Weather"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [ *  ]\n    Weather"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [*   ]\n    Weather"); sleep(0.5); lcd.clear()

loading_loop = Process(target=load_screen)

#LCD welcome
lcd.backlight(lcd.TEAL)
loading_loop.start()

#Load settings
zip_code = config.get('weather', 'zip')
hot = config.get('weather', 'hot')
cold = config.get('weather', 'cold')

sleep(1.5)

#Scrolling variables for ticker
BLANK = "               "
start = 0
end = 15
speed = 0.2

"""
Detect current city from connection

user_ip = urllib2.urlopen('http://myip.dnsdynamic.org/').read()
response = urllib2.urlopen('http://api.hostip.info/get_html.php?ip=%s&position=true' % user_ip).read()
"""

def get_weather(zip):
    return pywapi.get_weather_from_yahoo(str(zip), units='imperial')

def fill_space(line):
    if len(line)<16:
        for s in range(len(line)-16, 16):
            line += " "
    return line

def current_weather(results):
    c_loc = results['condition']['title'] + '\n'
    c_loc = c_loc[c_loc.index('for')+4:c_loc.index('at')-1]

    c_temp = results['condition']['temp']
    c_cond = results['condition']['text']
    c_hi = results['forecasts'][0]['high'] + 'F'
    c_lo = results['forecasts'][0]['low'] + 'F'
    c_hum = results['atmosphere']['humidity'] + '%'
    c_vis = results['atmosphere']['visibility'] + 'mi'

    weather_string = BLANK + "T: %sF, Hi: %s, Lo: %s - %s - %s humidity - %s visibility" % (c_temp, c_hi, c_lo, c_cond, c_hum, c_vis)

    return [c_loc, int(c_temp), weather_string]

def weekly_forecast(results):
    dt_line = ""; cond_line = ""
    for dow in results['forecasts']:
        day_dt = ""; cond_dt = ""
        if dow['day']=='Sun': day_dt='[Su] '
        elif dow['day']=='Mon': day_dt='[M] '
        elif dow['day']=='Tue': day_dt='[Tu] '
        elif dow['day']=='Wed': day_dt='[W] '
        elif dow['day']=='Thu': day_dt='[Th] '
        elif dow['day']=='Fri': day_dt='[F] '
        elif dow['day']=='Sat': day_dt='[Sa] '

        day_dt += 'Hi:%s Lo:%s' % (dow['high'], dow['low'])
        cond_dt = dow['text']

        dt_line += fill_space(day_dt)
        cond_line += fill_space(cond_dt)

    return [dt_line, cond_line]

try:
    results = get_weather(zip_code)
    current = current_weather(results)
    forecasts = weekly_forecast(results)
    connection = True
except:
    connection = False
    lcd.clear()
    lcd.message("Yahoo!    [fail]\n    Weather")

panel = 0
loading_loop.terminate()
while True:
    if lcd.buttonPressed(lcd.SELECT): break
    if connection:
        if panel == 0:
            #Switching between current weather and weekly forecast
            if lcd.buttonPressed(lcd.RIGHT): panel=1

            if start == len(current[2])+3:
                start=0; end=15

            if int(datetime.now().minute)%30==0 and int(datetime.now().second)==0:
                current = current_weather(get_weather(zip_code))
                print('Weather fetch')

            #Correspond backlight to cold, warm, hot
            if current[1] <= cold: lcd.backlight(lcd.BLUE)
            elif cold < current[1] < hot: lcd.backlight(lcd.YELLOW)
            else: lcd.backlight(lcd.RED)

            lcd.clear()
            lcd.message(current[0]+'\n'+current[2][start:end])
            start += 1; end += 1
            sleep(speed)
        #Weekly forecast
        elif panel == 1:
            sleep(1)
            lcd.clear()
            lcd.message(forecasts[0]+'\n'+forecasts[1])
            sleep(1)
            if lcd.buttonPressed(lcd.LEFT): panel=0