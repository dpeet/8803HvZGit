try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
from PIL import ImageTk
import webbrowser
import serial
import time
import MySQLdb
import RPi.GPIO as GPIO
import tkFont

root = Tk()
dentonlarge = tkFont.Font(family="Denton",size=36,weight="bold")
canvas = Canvas(width = 200, height = 200, bg = 'black')
HomeScreen = ImageTk.PhotoImage(file = "Pictures/Home_Screen.png")
Human1 = ImageTk.PhotoImage(file = "Pictures/Human_Stats_Screen.png")
Coin = ImageTk.PhotoImage(file = "Pictures/Blank_Coin_Screen.png")
Human2 = ImageTk.PhotoImage(file = "Pictures/Update_Human_Screen.png")
Zombie1 = ImageTk.PhotoImage(file = "Pictures/Zombie_Stat_Screen.png")
Zombie2 = ImageTk.PhotoImage(file = "Pictures/Update_Zombie_Screen.png")
runCoin = 1
def readPlayerID():
	port = serial.Serial('/dev/ttyUSB1', 2400, timeout=1)
	try:		
		tagid = port.read(12)
		if(len(tagid) != 0):
			# close and open the port to blink the light and give visual feedback
			port.close()
			tagid = tagid.strip()
			timestamp = time.time()
			print("Time:%s, Tag:%s" % (timestamp,tagid))			
			time.sleep(.5)
			port.open()
			return tagid;					

	except KeyboardInterrupt:
		port.close()
		##  db.commit()
		##  db.close()
		print ("Program interrupted")
	return;

def readRFID():
	port = serial.Serial('/dev/ttyUSB1', 2400, timeout=1)
	try:		
		tagid = port.read(12)
		if(len(tagid) != 0):
                        blinkRed(1)
			# close and open the port to blink the light and give visual feedback
			port.close()
			tagid = tagid.strip()
			timestamp = time.time()
			print("Time:%s, Tag:%s" % (timestamp,tagid))			
			time.sleep(.5)
			port.open()
			return tagid;					

	except KeyboardInterrupt:
		port.close()
		##  db.commit()
		##  db.close()
		print ("Program interrupted")
	return;
def createDisplay():
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	w, h = root.winfo_screenwidth(), root.winfo_screenheight()
	root.geometry("%dx%d+0+0" % (w, h-10))
	#root.overrideredirect(1)
	#root.geometry("%dx%d+0+0" % (w, h))
	#root.focus_set() # <-- move focus to this widget
	#root.bind("<Escape>", lambda e: e.widget.quit())
	#root.geometry("250x150+0+0")
	canvas.pack(expand = YES, fill = BOTH)
	canimage = canvas.create_image(0, 0, image = HomeScreen, anchor = NW)
	return canimage;

def blinkGreen(n):
   print ("writing")
   while(n>0):
      arduinoSerialData = serial.Serial('/dev/ttyUSB0',9600)
      arduinoSerialData.write('5')
      arduinoSerialData.close()
      time.sleep(.25)
      n-=1


def blinkRed(n):
   print ("writing")
   while(n>0):
      arduinoSerialData = serial.Serial('/dev/ttyUSB0',9600)
      arduinoSerialData.write('6')
      arduinoSerialData.close()
      time.sleep(.25)
      n-=1

    
def main():
	while 1:
		canimage = createDisplay()
		playerID = None
		while playerID is None:		
			root.update()
			playerID = readPlayerID()
		db=MySQLdb.connect("localhost","root","password","HvZ")
		cursor = db.cursor()
	 	cursor.execute("""select * from Players where playerID = %s""", (playerID))
		results = cursor.fetchall()
		row = results[0]
		playerID = row[0]
		RFID = row[1]
		status = row[2]
		killID = row[3]
		# Now print fetched result
		print "fname=%s,lname=%d" % (playerID, status)
		db.commit()
		cursor.close()
		db.close()
		if (status == 1):
                        blinkGreen(3)
			canvas.itemconfig(canimage, image = Human1)
			#canvas.create_image(0, 0, image = Human1, anchor = NW)
			pwmPin = 18 # Broadcom pin 18 (P1 pin 12)
			ledPin = 23 # Broadcom pin 23 (P1 pin 16)
			butPin = 17 # Broadcom pin 17 (P1 pin 11)

			dc = 95 # duty cycle (0-100) for PWM pin

			# Pin Setup:
			GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
			GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output
			GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
			pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency
			GPIO.setup(butPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Button pin set as input w/ pull-up

			# Initial state for LEDs:
			GPIO.output(ledPin, GPIO.LOW)
			pwm.start(dc)
			coins = 0
			GPIO.add_event_detect(butPin, GPIO.RISING)
			def readCoins():	
				try:
					if GPIO.event_detected(butPin): 
						pwm.ChangeDutyCycle(100-dc)
						#GPIO.output(ledPin, GPIO.HIGH)
						#time.sleep(0.075)
						#GPIO.output(ledPin, GPIO.LOW)
						#time.sleep(0.075)
						print("coin detected")
						blinkGreen(1)
						return 1;
					else:           
						pwm.ChangeDutyCycle(dc)
						#GPIO.output(ledPin, GPIO.LOW)
						#blinkRed(1)
						return 0;
				except KeyboardInterrupt:
					print ("Program interrupted")
					return 0;
			def breakcoin():
				global runCoin
				runCoin = 0
				print ("break working")
				return;
			b = Button(root, command=breakcoin, anchor = W)
			button1_window = canvas.create_window(150, 600, anchor=NW, window=b)
			global runCoin
			canvas_id = canvas.create_text(250, 350, anchor=NW)
			canvas.itemconfig(canvas_id, text="", font = dentonlarge, fill = 'yellow')
			#canvas.i(canvas_id, 0, " ")
			#canvas.delete(canvas_id, 0)
			#text = Text(root, font=dentonlarge)
			#text.insert('1.0', str(coins))
			#text_window = canvas.create_window(50, 50, anchor=NW, window=text)
			while (runCoin == 1):
				root.update()
				coins += readCoins()
				if (coins == 1):
					canvas.itemconfig(canimage, image = Coin)
					b.configure(activebackground = "#03122b", text="Done >", background = "#032e72", foreground = "white", activeforeground = "white", relief = FLAT, font = dentonlarge)
					#canvas.create_image(0, 0, image = Coin, anchor = NW)
				#canvas.delete(canvas_id, 0)
				if (coins >0):
					canvas.itemconfig(canvas_id, text = str(coins))
				#text.delete('1.0')
				#text.insert('1.0', str(coins))

			if (coins > 0):
				db=MySQLdb.connect("localhost","root","password","HvZ")
				cursor = db.cursor()
				timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
				cursor.execute("""insert into Humans values (%s, %s, %s)""", (playerID, coins, timestamp))
				db.commit()
				cursor.close()
				db.close()
			pwm.stop() # stop PWM
			GPIO.cleanup() # cleanup all GPIO
			canvas.itemconfig(canimage, image = Human2)
			#canvas.create_image(0, 0, image = Human2, anchor = NW)
			b.destroy()
			canvas.delete(canvas_id)
			runCoin = 1;
			root.update()
			time.sleep(4)
		else:
                        blinkRed(3)
			canvas.itemconfig(canimage, image = Zombie1)
			#canvas.create_image(0, 0, image = Zombie1, anchor = NW)
			rfid = None
			while rfid is None:
				root.update()
				rfid = readRFID()
			db=MySQLdb.connect("localhost","root","password","HvZ")
			cursor = db.cursor()
			timestamp = time.strftime('%Y-%m-%d %H:%M:%S')				
			cursor.execute("""insert into Zombies values (%s, %s, %s)""", (playerID, rfid, timestamp))
			#cursor.execute("""update Players set status = 2 where killID = %s""", (rfid))
			time.sleep(.5)
			db.commit()
			cursor.close()
			db.close()
			canvas.itemconfig(canimage, image = Zombie2)
			#canvas.create_image(0, 0, image = Zombie2, anchor = NW)
			root.update()
			time.sleep(5)

if __name__ == '__main__':
	main()
