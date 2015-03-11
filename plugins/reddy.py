import praw
from time import sleep
from datetime import datetime
from multiprocessing import Process


def load_screen():
    lcd.clear()
    while True:
        lcd.message("Reddit    [*   ]\n    Headlines"); sleep(0.2); lcd.clear()
        lcd.message("Reddit    [ *  ]\n    Headlines"); sleep(0.2); lcd.clear()
        lcd.message("Reddit    [  * ]\n    Headlines"); sleep(0.2); lcd.clear()
        lcd.message("Reddit    [   *]\n    Headlines"); sleep(0.2); lcd.clear()
        lcd.message("Reddit    [  * ]\n    Headlines"); sleep(0.2); lcd.clear()
        lcd.message("Reddit    [ *  ]\n    Headlines"); sleep(0.2); lcd.clear()


def update(n):
    submissions = r.get_subreddit(subreddits[subreddit_index]).get_hot(limit=n)
    hl_string = ""

    while True:
        try:
            headline = str(submissions.next())
            hl_string += BLANK + headline[headline.index(':')+3:]
        except:
            break

    return hl_string

#Settings
r = praw.Reddit(user_agent="Reddit 0.1")
subreddits = config.get('reddy', 'list').split(',')
num_of_headlines = int(config.get('reddy', 'headlines'))
subreddit_index = 0

#Scrolling variables for ticker
BLANK = "               "
start = 0
end = 15
speed = 0.1

#Loading screen
lcd.message("Reddit\n    Headlines")
lcd.backlight(lcd.GREEN)
loading_loop = Process(target=load_screen)
sleep(1)

loading_loop.start()

try:
    headlines = update(num_of_headlines)
    title = '[' + subreddits[subreddit_index] + ']\n'
except:
    lcd.clear()
    lcd.message("Reddit    [fail]\n     Headlines")

loading_loop.terminate()

#Main Loop
while True:
    if lcd.buttonPressed(lcd.SELECT): 
        break
    if start == len(headlines)+3:
        end = 15; start = 0

    on_hour = int(datetime.now().minute) == 0
    zero_seconds = int(datetime.now().second) == 0
    if on_hour and zero_seconds:
        headlines = update(num_of_headlines)

    btn_up = lcd.buttonPressed(lcd.UP)
    btn_down = lcd.buttonPressed(lcd.DOWN)
    if btn_up or btn_down:
        if btn_up and speed > 0.1:
            if speed == 0.2:
                speed = 0.1
            else:
                speed = 0.2
        elif btn_down and speed < 0.3:
            if speed == 0.2:
                speed = 0.3
            else:
                speed = 0.2

    #change subreddit
    if lcd.buttonPressed(lcd.LEFT) or lcd.buttonPressed(lcd.RIGHT):
        if lcd.buttonPressed(lcd.LEFT):
            if subreddit_index == 0:
                subreddit_index = len(subreddits) - 1
            else:
                subreddit_index -= 1
        elif lcd.buttonPressed(lcd.RIGHT):
            if subreddit_index == len(subreddits) - 1:
                subreddit_index = 0
            else:
                subreddit_index += 1
        #TODO: Enable subreddit caching to reduce requests
        headlines = update(num_of_headlines)
        end = 15; start = 0
        title = '[' + subreddits[subreddit_index] + ']\n'

    lcd.clear()
    lcd.message(title + headlines[start:end])
    start += 1
    end += 1

    sleep(speed)