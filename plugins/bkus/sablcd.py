import requests
import threading, ctypes
from multiprocessing import Process
from time import sleep

#LCD welcome
lcd.backlight(lcd.YELLOW)
lcd.message("SABlcd\n SABnzbd tracker")
sleep(1.5)

#API info
host = config.get('sablcd', 'host')
port = config.get('sablcd', 'port')
key = config.get('sablcd', 'key')
url = 'http://%s:%s/api?mode=queue&output=json&apikey=%s' % (host, port, key)

connection = False
 
#Exit handler
def exit_handler():
	display_loop.terminate()

#Request queue info from constructed URL
def get_status():
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
def show_status(info, panel):
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

#Display loop
def run_display():
	counter = 0
	panel = 1
	while True:
		sleep(1)
		counter += 1
					
		if counter == 5:
			counter = 0; panel += 1
			if panel == 4:
				panel = 1
		try: show_status(get_status(), panel)
		except: lcd.clear(); lcd.message("No Connection")
			
display_loop = Process(target=run_display)
display_loop.start()

#Exit plugin on trigger
while True:
	if lcd.buttonPressed(lcd.SELECT):
		break
	
exit_handler()