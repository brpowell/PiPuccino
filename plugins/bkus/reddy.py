import praw
from time import sleep
from datetime import datetime
from multiprocessing import Process

def load_screen():
    while True:
        lcd.message("Reddy    [*   ]\nReddit headlines"); sleep(0.5); lcd.clear()
        lcd.message("Reddy    [ *  ]\nReddit headlines"); sleep(0.5); lcd.clear()
        lcd.message("Reddy    [  * ]\nReddit headlines"); sleep(0.5); lcd.clear()
        lcd.message("Reddy    [   *]\nReddit headlines"); sleep(0.5); lcd.clear()
        lcd.message("Reddy    [  * ]\nReddit headlines"); sleep(0.5); lcd.clear()
        lcd.message("Reddy    [ *  ]\nReddit headlines"); sleep(0.5); lcd.clear()
        lcd.message("Reddy    [*   ]\nReddit headlines"); sleep(0.5); lcd.clear()

loading_loop = Process(target=load_screen)

#LCD welcome & Reddit setup
r = praw.Reddit(user_agent="Reddy 0.1")
lcd.backlight(lcd.GREEN)
loading_loop.start()
sleep(1.5)

#Scrolling variables for ticker
BLANK = "               "
start = 0
end = 15
speed = 0.1

subreddits = config.get('reddy', 'list').split(',')
subreddit_index = 0

#Exit handler
#def exit_handler():

#Generate string of n headlines and return it
def update(n):
	current_subreddit = subreddits[subreddit_index]
	submissions = r.get_subreddit(subreddits[subreddit_index]).get_hot(limit=n)
	headlines = ""
    
	while True:
		try:
			headline = str(submissions.next())
			headlines += BLANK + headline[headline.index(':')+3:]
		except:
			break
			
	return headlines

headlines = update(5)
title = '[' + subreddits[subreddit_index] + ']\n'
loading_loop.terminate()
while True:
	#switch story
	if start == len(headlines)+3:
		end = 15; start = 0

	#update every 10 minutes
	if int(datetime.now().minute) == 0: headlines = update(5)
	
	#changing speeds
	if lcd.buttonPressed(lcd.UP) or lcd.buttonPressed(lcd.DOWN):
		if lcd.buttonPressed(lcd.UP) and speed>0.1:
			if speed == 0.2: speed = 0.1
			else: speed = 0.2
		elif lcd.buttonPressed(lcd.DOWN) and speed<0.3:
			if speed == 0.2: speed = 0.3
			else: speed = 0.2
		#print(speed)
    
	#change subreddit
	if lcd.buttonPressed(lcd.LEFT) or lcd.buttonPressed(lcd.RIGHT):
		if lcd.buttonPressed(lcd.LEFT):
			if subreddit_index==0: subreddit_index = 4
			else: subreddit_index -= 1
		elif lcd.buttonPressed(lcd.RIGHT):
			if subreddit_index==4: subreddit_index = 0
			else: subreddit_index += 1
			
		headlines = update(5)
		end = 15; start = 0
		title = '[' + subreddits[subreddit_index] + ']\n'
	
	#Exit plugin on trigger
	if lcd.buttonPressed(lcd.SELECT): break

	#print
	lcd.clear()
	lcd.message(title + headlines[start:end])
	start += 1
	end += 1
	
	sleep(speed)
	
#exit_handler()