#!/usr/bin/python



#This code will open socket port 5025 and send *IDN to instrument.

import time
import socket
import math
import numpy as np
#import mysql.connector

'''db = mysql.connector.connect(host="localhost",  # this PC
		     user="root",         # this user only has access to CPTLAB database
                     passwd="Teleport1536!",  # your password
		     auth_plugin='mysql_native_password',
		     database="teleportcommission") # name of the data base
'''

input_buffer = 4096 #Temp buffer for rec data.
exRat = 0


pna = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pna.connect(("192.168.2.200", 5025))
#pna.connect(("192.168.0.177", 5025))




idn = "*IDN?" + "\n"
idn = idn.encode()
pna.send(idn)

id = pna.recv(input_buffer).decode()

print(id)
#cur = db.cursor()

#cur.execute("SHOW TABLES")

#for x in cur:
#  print(x)

i=1
max_meas = "meas:vmax? CHAN2" + "\n"
max_meas = max_meas.encode()
min_meas = "meas:vmin? CHAN2" + "\n"
min_meas = min_meas.encode()

mins = []
maxs = []


while i<=5400:
	pna.send(max_meas)
	maxs.append(pna.recv(input_buffer).decode())
	pna.send(min_meas)
	mins.append(pna.recv(input_buffer).decode())

	#query = "INSERT INTO interf(Vmax0, Vmax1, Vmax2, datetime) values("+str(vmax0)+ ","+ str(vmax1)+ ","+ str(vmax2)+", NOW());"
	#query = "INSERT INTO teleportcommission (Vmax0, Vmax1,) values("+str(vmax0)+ ","+ str(vmax1)+ ", NOW());"
#	cur.execute(query)
#	db.commit()
#	print(cur.rowcount, "record inserted.")

	i +=1
	time.sleep(1)


np.save("Bob_IM_min_max_no_power",[mins,maxs])
pna.close()
