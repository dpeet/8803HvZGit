import serial
import time
import MySQLdb
import RPi.GPIO as GPIO
import time
port = serial.Serial('/dev/ttyUSB1', 2400, timeout=1)
try:
    print ("start")
    playerID = None
    killID = None
    while 1:
        tagid = port.read(12)
        if(len(tagid) != 0):
            break
    # close and open the port to blink the light and give visual feedback
    port.close()
    playerID = tagid.strip()
    timestamp = time.time()
    print("Time:%s, Tag:%s" % (timestamp,playerID))
    time.sleep(.5)
    port.open()
    while 1:
        tagid = port.read(12)
        if(len(tagid) != 0):
            break
        # close and open the port to blink the light and give visual feedback
    port.close()
    killID = tagid.strip()
    timestamp = time.time()
    print("Time:%s, Tag:%s" % (timestamp,killID))
    time.sleep(.5)
    port.open()

    db=MySQLdb.connect("localhost","root","password","HvZ")
    cursor = db.cursor()
    #cursor.execute("""select * from Players where playerID = %s""", (playerID))				
    cursor.execute("""insert into Players values (%s, %s, %s, %s)""", (playerID, playerID, 1, killID))
    #results = cursor.fetchall()
	#row = results[0]
	#playerID = row[0]
	#RFID = row[1]
	#status = row[2]
	#killID = row[3]
	# Now print fetched result
    print "fname=%s,lname=%s" % (playerID, killID)
    db.commit()
    cursor.close()
    db.close()

except KeyboardInterrupt:
    port.close()
    ##  db.commit()
    ##  db.close()
    print ("Program interrupted")
