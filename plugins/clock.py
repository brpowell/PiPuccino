from datetime import datetime
from time import sleep
from multiprocessing import Process


def clock_display():
    global display
    while True:
        if display:
            lcd.clear()
            now = datetime.now()
            date = now.strftime('%a %b %d')
            time = now.strftime('     %I:%M:%S %p')
            lcd.message(date+'\n'+time)
            sleep(1)


lcd.backlight(lcd.VIOLET)
lcd.message("Clock")
sleep(1)

display = True

clock_loop = Process(target=clock_display)
clock_loop.start()

while True:
    if lcd.buttonPressed(lcd.SELECT):
        break

clock_loop.terminate()
