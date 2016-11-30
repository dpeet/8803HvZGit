import serial
import time
import MySQLdb
import RPi.GPIO as GPIO
import time
port = serial.Serial('/dev/ttyUSB0', 2400, timeout=1)
try:
	while True:
	  # attempt to read in a tag
	  tagid = port.read(12)
	  if(len(tagid) != 0):
	  	break

    port.close()
    playerID = tagid.strip()
    timestamp = time.time()
    port.open()    
    print("Time:%s, Tag:%s" % (timestamp,playerID))
    while True:
    	# attempt to read in a tag
		tagid = port.read(12)
		if(len(tagid) != 0):
	  		break
	port.close()
    killID = tagid.strip()
    timestamp = time.time()
    port.open()
    print("Time:%s, Tag:%s" % (timestamp,killID))
    db=MySQLdb.connect("localhost","root","password","HvZ")
	cursor = db.cursor()
    cursor.execute("""insert into Players values (%s, %s, %s, %s)""", (playerID, playerID, 1, killID ))
      # Now print fetched result
    print "playerID=%s,killID=%d" % (playerID, killID)
    time.sleep(.5)
    port.open()
	db.commit()
	cursor.close()
	db.close()
	port.close()

except KeyboardInterrupt:
	port.close()
	##  db.commit()
	##  db.close()
	print ("Program interrupted")
