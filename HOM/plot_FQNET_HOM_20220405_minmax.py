#!/usr/bin/python2.7

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib as mpl
#import tkinter
#matplotlib.use('TkAgg')
import datetime
import math
import pymysql
import os
import time
import pandas as pd
delay_step_time = 1
adqtime_tab2=1
adqtime_histo=1


START_TIME = '2022-04-05 15:43:00'
END_TIME = '2022-04-05 16:41:00'

#START_TIME = '2019-12-11 12:14:00'
#END_TIME = '2019-12-11 14:47:54'


#connect to database


and1=[]
bufferand1=[]
bufferand2=[]
bufferand3=[]
and2 = []
and3 = []
or_gate = []
bufferor_gate=[]
bsm1 = []
bufferbsm1=[]
bsm2 = []
bufferbsm2=[]

Ra1=[]
Rb1=[]
Rc1=[]
Ra2=[]
Rb2=[]
Rc2=[]
Ra3=[]
Rb3=[]
Rc3=[]
time_tab2=[]
time_histo=[]

T_Vap = []
T_Vin = []


max_two_fold = 0
max_two_fold_norm = 0

max_three_fold = 0
max_three_fold_norm = 0

rc_max = 0

try:
	db_gui = pymysql.connect(host="192.168.2.3",
						 user="GUI2",
						 passwd="Teleport1536!",  # your password
						 db="INQNET_GUI")
						 #charset='utf8mb4')
	with db_gui.cursor(pymysql.cursors.DictCursor) as cur:
		TABLE_NAME = "inqnet_gui_tab2gates_V3"
		queryGUI = "SELECT and1, and2, and3,orgate, bsm1, bsm2, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()

		while row is not None:

			and1.append(row["and1"])
			and2.append(row["and2"])
			and3.append(row["and3"])
			bsm1.append(row["bsm1"])
			bsm2.append(row["bsm2"])
			or_gate.append(row["orgate"])
			time_tab2.append(row["datetime"])
			#print
			row = cur.fetchone()

		TABLE_NAME = "inqnet_gui_historates"
		queryGUI = "SELECT Ra1, Rb1, Rc1, Ra2, Rb2, Rc2, Ra3, Rb3,Rc3, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			Ra1.append(row["Ra1"])
			Rb1.append(row["Rb1"])
			Rc1.append(row["Rc1"])
			Ra2.append(row["Ra2"])
			Rb2.append(row["Rb2"])
			Rc2.append(row["Rc2"])
			Ra3.append(row["Ra3"])
			Rb3.append(row["Rb3"])
			Rc3.append(row["Rc3"])
			time_histo.append(row["datetime"])
			row = cur.fetchone()
	db_gui.close()



	time_tab2_first = str(time_tab2[0])
	print("time_tab2_first=",time_tab2_first )
	time_tab2_last = str(time_tab2[-1])

	first_time_tab2 = datetime.datetime.strptime(time_tab2_first,'%Y-%m-%d %H:%M:%S')
	time_tab2_dt = []
	time_tab2_el_mins = []
	time_tab2_el = []

	time_histo_first = str(time_histo[0])
	print("time_histo_first=",time_histo_first )
	time_histo_last = str(time_histo[-1])

	first_time_histo = datetime.datetime.strptime(time_histo_first,'%Y-%m-%d %H:%M:%S')
	time_histo_dt = []
	time_histo_el_mins = []
	time_histo_el = []


	for t in time_tab2:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_tab2
		time_tab2_dt.append(datime)#.time)
		time_tab2_el.append(elapsed.total_seconds())
		time_tab2_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
	for t in time_histo:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_histo
		time_histo_dt.append(datime)#.time)
		time_histo_el.append(elapsed.total_seconds())
		time_histo_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes






	time_histo_el=np.array(time_histo_el)
	time_tab2_el=np.array(time_tab2_el)


	fig, axs = plt.subplots(5,1, sharex=True)
	ax = axs[0]
	ax.plot(time_histo_el_mins, Ra1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Ra1")
	ax = axs[1]
	ax.plot(time_histo_el_mins, Rb1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Rb1")
	ax = axs[2]
	ax.plot(time_histo_el_mins, Rc1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Rc1")
	ax = axs[3]
	ax.plot(time_tab2_el_mins, and2)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("and2")
	ax = axs[4]
	ax.plot(time_tab2_el_mins, bsm1)
	ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("bsm1")
	plt.show()

	Ra1 = np.array(Ra1)
	Rb1 = np.array(Rb1)
	Rc1 = np.array(Rc1)
	and2 = np.array(and2)

	boolArr = np.argwhere(Rb1<5200)
	print(len(boolArr))

	time_histo_el_mins_moded = np.array([time_histo_el_mins[i[0]] for i in boolArr])
	time_tab2_el_mins_moded = np.array([time_tab2_el_mins[i[0]] for i in boolArr])

	#time_histo_el_mins_moded = np.where(Ra1<7000,Ra1,time_histo_el_mins_moded)
	#time_tab2_el_mins_moded = np.where(Ra1<7000,Ra1,time_tab2_el_mins_moded)
	Ra1 = np.array([Ra1[i[0]] for i in boolArr])
	Rc1 = np.array([Rc1[i[0]] for i in boolArr])
	and2 = np.array([and2[i[0]] for i in boolArr])
	bsm1 = np.array([bsm1[i[0]] for i in boolArr])
	Rb1 = np.array([Rb1[i[0]] for i in boolArr])

	print(Ra1)
	print(Rb1)

	fig, axs = plt.subplots(5,1, sharex=True)
	ax = axs[0]
	ax.plot(time_histo_el_mins_moded, Ra1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Ra1")
	ax = axs[1]
	ax.plot(time_histo_el_mins_moded, Rb1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Rb1")
	ax = axs[2]
	ax.plot(time_histo_el_mins_moded, Rc1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Rc1")
	ax = axs[3]
	ax.plot(time_tab2_el_mins_moded, and2)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("and2")
	ax = axs[4]
	ax.plot(time_tab2_el_mins_moded, bsm1)
	ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("bsm1")
	plt.show()

	max_two_fold = np.sum(and2)
	max_three_fold = np.sum(bsm1)

	max_two_fold_norm = np.sum(and2/Rb1)*np.mean(Rb1)
	max_three_fold_norm = np.sum(bsm1/Rb1)*np.mean(Rb1)

	rb_max = np.mean(Rb1)
	rc_max = np.mean(Rc1)

	time_max = len(Rb1)

	print("------Non-Normalized Max Counts------")
	print("Two Fold {}".format(max_two_fold))
	print("Three Fold {}".format(max_three_fold))
	print("------Normalized Max Counts------")
	print("Two Fold {}".format(max_two_fold_norm))
	print("Three Fold {}".format(max_three_fold_norm))


except KeyboardInterrupt:
 	print("Quit")


START_TIME = '2022-04-05 14:24:00'
END_TIME = '2022-04-05 15:40:00'

#START_TIME = '2019-12-11 12:14:00'
#END_TIME = '2019-12-11 14:47:54'


#connect to database


and1=[]
bufferand1=[]
bufferand2=[]
bufferand3=[]
and2 = []
and3 = []
or_gate = []
bufferor_gate=[]
bsm1 = []
bufferbsm1=[]
bsm2 = []
bufferbsm2=[]

Ra1=[]
Rb1=[]
Rc1=[]
Ra2=[]
Rb2=[]
Rc2=[]
Ra3=[]
Rb3=[]
Rc3=[]
time_tab2=[]
time_histo=[]

T_Vap = []
T_Vin = []

min_two_fold = 0
min_two_fold_norm = 0

min_three_fold = 0
min_three_fold_norm = 0

rc_min = 0

try:
	db_gui = pymysql.connect(host="192.168.2.3",
						 user="GUI2",
						 passwd="Teleport1536!",  # your password
						 db="INQNET_GUI")
						 #charset='utf8mb4')
	with db_gui.cursor(pymysql.cursors.DictCursor) as cur:
		TABLE_NAME = "inqnet_gui_tab2gates_V3"
		queryGUI = "SELECT and1, and2, and3,orgate, bsm1, bsm2, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()

		while row is not None:

			and1.append(row["and1"])
			and2.append(row["and2"])
			and3.append(row["and3"])
			bsm1.append(row["bsm1"])
			bsm2.append(row["bsm2"])
			or_gate.append(row["orgate"])
			time_tab2.append(row["datetime"])
			#print
			row = cur.fetchone()

		TABLE_NAME = "inqnet_gui_historates"
		queryGUI = "SELECT Ra1, Rb1, Rc1, Ra2, Rb2, Rc2, Ra3, Rb3,Rc3, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()
		while row is not None:
			Ra1.append(row["Ra1"])
			Rb1.append(row["Rb1"])
			Rc1.append(row["Rc1"])
			Ra2.append(row["Ra2"])
			Rb2.append(row["Rb2"])
			Rc2.append(row["Rc2"])
			Ra3.append(row["Ra3"])
			Rb3.append(row["Rb3"])
			Rc3.append(row["Rc3"])
			time_histo.append(row["datetime"])
			row = cur.fetchone()
	db_gui.close()



	time_tab2_first = str(time_tab2[0])
	print("time_tab2_first=",time_tab2_first )
	time_tab2_last = str(time_tab2[-1])

	first_time_tab2 = datetime.datetime.strptime(time_tab2_first,'%Y-%m-%d %H:%M:%S')
	time_tab2_dt = []
	time_tab2_el_mins = []
	time_tab2_el = []

	time_histo_first = str(time_histo[0])
	print("time_histo_first=",time_histo_first )
	time_histo_last = str(time_histo[-1])

	first_time_histo = datetime.datetime.strptime(time_histo_first,'%Y-%m-%d %H:%M:%S')
	time_histo_dt = []
	time_histo_el_mins = []
	time_histo_el = []


	for t in time_tab2:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_tab2
		time_tab2_dt.append(datime)#.time)
		time_tab2_el.append(elapsed.total_seconds())
		time_tab2_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
	for t in time_histo:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_histo
		time_histo_dt.append(datime)#.time)
		time_histo_el.append(elapsed.total_seconds())
		time_histo_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes






	time_histo_el=np.array(time_histo_el)
	time_tab2_el=np.array(time_tab2_el)


	fig, axs = plt.subplots(5,1, sharex=True)
	ax = axs[0]
	ax.plot(time_histo_el_mins, Ra1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Ra1")
	ax = axs[1]
	ax.plot(time_histo_el_mins, Rb1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Rb1")
	ax = axs[2]
	ax.plot(time_histo_el_mins, Rc1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Rc1")
	ax = axs[3]
	ax.plot(time_tab2_el_mins, and2)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("and2")
	ax = axs[4]
	ax.plot(time_tab2_el_mins, bsm1)
	ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("bsm1")
	plt.show()

	Ra1 = np.array(Ra1)
	Rb1 = np.array(Rb1)
	Rc1 = np.array(Rc1)
	and2 = np.array(and2)

	boolArr = np.argwhere(Rb1<5200)
	print(len(boolArr))

	time_histo_el_mins_moded = np.array([time_histo_el_mins[i[0]] for i in boolArr])
	time_tab2_el_mins_moded = np.array([time_tab2_el_mins[i[0]] for i in boolArr])

	#time_histo_el_mins_moded = np.where(Ra1<7000,Ra1,time_histo_el_mins_moded)
	#time_tab2_el_mins_moded = np.where(Ra1<7000,Ra1,time_tab2_el_mins_moded)
	Ra1 = np.array([Ra1[i[0]] for i in boolArr])
	Rc1 = np.array([Rc1[i[0]] for i in boolArr])
	and2 = np.array([and2[i[0]] for i in boolArr])
	bsm1 = np.array([bsm1[i[0]] for i in boolArr])
	Rb1 = np.array([Rb1[i[0]] for i in boolArr])

	print(Ra1)
	print(Rb1)

	fig, axs = plt.subplots(5,1, sharex=True)
	ax = axs[0]
	ax.plot(time_histo_el_mins_moded, Ra1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Ra1")
	ax = axs[1]
	ax.plot(time_histo_el_mins_moded, Rb1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Rb1")
	ax = axs[2]
	ax.plot(time_histo_el_mins_moded, Rc1)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("Rc1")
	ax = axs[3]
	ax.plot(time_tab2_el_mins_moded, and2)
	#ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("and2")
	ax = axs[4]
	ax.plot(time_tab2_el_mins_moded, bsm1)
	ax.set_xlabel("Elapsed time (min)")
	ax.set_ylabel("bsm1")
	plt.show()

	min_two_fold = np.sum(and2)
	min_three_fold = np.sum(bsm1)

	min_two_fold_norm = np.sum(and2/Rb1)*np.mean(Rb1)
	min_three_fold_norm = np.sum(bsm1/Rb1)*np.mean(Rb1)

	rb_min = np.mean(Rb1)
	rc_min = np.mean(Rc1)

	rc_scaling = rc_max/rc_min
	rb_scaling = rb_max/rb_min

	time_min = len(Rb1)

	time_scaling = time_min/time_max



	print("------Non-Normalized Min Counts------")
	print("Two Fold {}".format(min_two_fold))
	print("Three Fold {}".format(min_three_fold))
	print("------Normalized Min Counts------")
	print("Two Fold {}".format(min_two_fold_norm))
	print("Three Fold {}".format(min_three_fold_norm))

	print("\n")



	print("------Non-Normalized------")
	print("-----Two-Fold HOM Visibility-----")
	print(1-min_two_fold/(max_two_fold*time_scaling))
	print("-----Three-Fold HOM Visibility-----")
	print(1-min_three_fold/(max_three_fold*time_scaling))

	print("------Rc Normalized------")
	print("-----Two-Fold HOM Visibility-----")
	print(1-min_two_fold*rc_scaling/(max_two_fold*time_scaling))
	print("-----Three-Fold HOM Visibility-----")
	print(1-min_three_fold*rc_scaling/(max_three_fold*time_scaling))

	print("------Rb Normalized Element------")
	print("-----Two-Fold HOM Visibility-----")
	print(1-min_two_fold_norm/(max_two_fold_norm*time_scaling))
	print("-----Three-Fold HOM Visibility-----")
	print(1-min_three_fold_norm/(max_three_fold_norm*time_scaling))

	print("------Rb Normalized Mean------")
	print("-----Two-Fold HOM Visibility-----")
	print(1-min_two_fold*rb_scaling/(max_two_fold*time_scaling))
	print("-----Three-Fold HOM Visibility-----")
	print(1-min_three_fold*rb_scaling/(max_three_fold*time_scaling))

except KeyboardInterrupt:
	print("Quit")
