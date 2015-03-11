import pywapi
from time import sleep
from datetime import datetime
from multiprocessing import Process


def load_screen():
    lcd.clear()
    while True:
        lcd.message("Yahoo!    [*   ]\n    Weather"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [ *  ]\n    Weather"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [  * ]\n    Weather"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [   *]\n    Weather"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [  * ]\n    Weather"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [ *  ]\n    Weather"); sleep(0.2); lcd.clear()
        #lcd.message("Yahoo!    [*   ]\n    Weather"); sleep(0.2); lcd.clear()


def get_weather(z):
    """Fetches weather from Yahoo! @rtype : dictionary"""
    return pywapi.get_weather_from_yahoo(str(z), units='imperial')


def fill_space(line):
    """Returns line with extra white space @rtype : str"""
    if len(line) < 16:
        for s in range(len(line)-16, 16):
            line += " "
    return line


def current_weather(r):
    """Fetch current weather and parse @rtype : list"""

    c_loc = r['condition']['title'] + '\n'
    c_loc = c_loc[c_loc.index('for')+4:c_loc.index('at')-1]

    c_temp = r['condition']['temp']
    c_cond = r['condition']['text']
    c_hi = r['forecasts'][0]['high'] + 'F'
    c_lo = r['forecasts'][0]['low'] + 'F'
    c_hum = r['atmosphere']['humidity'] + '%'
    c_vis = r['atmosphere']['visibility'] + 'mi'

    weather_string = BLANK + "T: %sF, Hi: %s, Lo: %s - %s - %s humidity - %s visibility" % (c_temp, c_hi, c_lo, c_cond, c_hum, c_vis)

    return [c_loc, int(c_temp), weather_string]


def weekly_forecast(r):
    #TODO: Weekly forecast
    """Generates top line and bottom line for LCD. Top line contains day and temps
        while the bottom line contains condition for each day @rtype : list"""
    dt_line = ""; cond_line = ""
    for dow in r['forecasts']:
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


#Settings
zip_code = config.get('yweather', 'zip')
hot = int(config.get('yweather', 'hot'))
cold = int(config.get('yweather', 'cold'))
panel = 0

#Scrolling variables for ticker
BLANK = "               "
start = 0
end = 15
speed = 0.2

#Starting up
lcd.message("Yahoo!\n    Weather")
lcd.backlight(lcd.TEAL)
loading_loop = Process(target=load_screen)
sleep(1.5)
loading_loop.start()

try:
    results = get_weather(zip_code)
    current = current_weather(results)
    forecasts = weekly_forecast(results)
    connection = True
except:
    connection = False
    lcd.clear()
    lcd.message("Yahoo!    [fail]\n    Weather")

loading_loop.terminate()

#Main Loop
while True:
    if connection:
        #Current weather panel
        if panel == 0:
            if lcd.buttonPressed(lcd.RIGHT):
                panel = 1

            if start == len(current[2])+3:
                start = 0; end = 15

            half_hour = int(datetime.now().minute) % 30 == 0
            zero_seconds = int(datetime.now().second) == 0
            if half_hour and zero_seconds:
                current = current_weather(get_weather(zip_code))
                print('Weather fetch')

            if current[1] <= cold:
                lcd.backlight(lcd.BLUE)
            elif cold < current[1] < hot:
                lcd.backlight(lcd.YELLOW)
            else:
                lcd.backlight(lcd.RED)

            lcd.clear()
            lcd.message(current[0]+'\n'+current[2][start:end])
            start += 1; end += 1
            sleep(speed)

    if lcd.buttonPressed(lcd.SELECT): break