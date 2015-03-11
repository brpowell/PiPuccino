import requests
import atexit
from time import sleep
#from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
 
#API info
host = '127.0.0.1'
port = '8080'
key = 'e514f47604e599fee3e464230f4895a1'
url = 'http://%s:%s/api?mode=queue&output=json&apikey=%s' % (host, port, key)
 
#Prepare LCD and display welcome message
#lcd = Adafruit_CharLCDPlate()
lcd.backlight(lcd.YELLOW)
lcd.message("SABlcd\n SABnzbd tracker")
sleep(3)

def getStatus():
	#Request queue info from constructed URL
	r = requests.get(url)
	info = r.json()['queue']
 
	#Extract global info of queue
	slots = info['noofslots']
	state = info['status']
	speed = str(int(float(info['kbpersec']))) + ' kb/s'
	
	#Extract info of first download slot in queue
	try:
		job = info['slots'][0]
		job_name = job['filename'][:16]
		
		job_mbtotal = int(float(job['mb']))
		job_mb = job_mbtotal - int(float(job['mbleft']))
		job_mbstatus = str(job_mb) + '/' + str(job_mbtotal) + 'MB'
		
		job_timeleft = job['timeleft']
		job_percent = job['percentage'] + '%'
	except IndexError:
		job_name = "No Active Slots"
		job_mbstatus  = "0/0 MB"
		job_timeleft = "0:00:0"
		job_percent = "0%"
	
	#Return collected data in list format
	return [slots, state, speed, job_name, job_mbstatus, job_timeleft, job_percent]
 
#Outputs collected data to LCD
def showStatus(info, panel):
	lcd.clear()
	if panel == 1:
		lcd.message("Queue: %s\n" % info[0])
		lcd.message(info[1])
	elif panel == 2:
		lcd.message("%s\n" % info[3])
		lcd.message(info[4])
	elif panel == 3:
		lcd.message("Left: %s\n" % info[5])
		lcd.message("%s %s" % (info[6],info[2]))

def exit_handler():
	print "SABlcd has shutdown"
	lcd.backlight(lcd.OFF)
	lcd.clear()
 
counter = 0
panel = 1
 
#Loop for displaying info. Changes panel every x seconds where counter=x
while True:
	sleep(1)
	counter += 1
	
	if lcd.buttonPressed(lcd.SELECT): break
		
	if counter == 10:
		counter = 0; panel += 1
		if panel == 4:
			panel = 1
			
	showStatus(getStatus(), panel)
	
exit_handler()
