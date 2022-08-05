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
adqtime_tab2=2
adqtime_tab1=2


START_TIME_tab1 = '2022-04-09 23:20:00'
END_TIME_tab1 = '2022-04-10 02:00:00'
START_TIME_tab2 = '2022-04-09 23:20:00'
END_TIME_tab2 = '2022-04-10 02:00:00'


#connect to database


A0,A1,A2 = [],[],[]
B0,B1,B2=[],[],[]
C0,C1,C2=[],[],[]
D0,D1,D2 = [],[],[]

ch0,ch1,ch2,ch3,ch4,ch5 =[],[],[],[],[],[]


time_tab1,time_tab2=[],[]



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
		TABLE_NAME = "TAB109_04_2022_22_59_24"
		queryGUI = "SELECT A0, A1, A2, B0, B1, B2, C0, C1, C2,D0, D1, D2, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME_tab1,END_TIME_tab1,))
		row = cur.fetchone()
		while row is not None:
			A0.append(row["A0"])
			B0.append(row["B0"])
			C0.append(row["C0"])
			D0.append(row["D0"])
			A1.append(row["A1"])
			B1.append(row["B1"])
			C1.append(row["C1"])
			D1.append(row["D1"])
			A2.append(row["A2"])
			B2.append(row["B2"])
			C2.append(row["C2"])
			D2.append(row["D2"])
			time_tab1.append(row["datetime"])
			row = cur.fetchone()


		TABLE_NAME = "TAB209_04_2022_22_59_24"
		queryGUI = "SELECT ch0, ch1, ch2, ch3, ch4, ch5, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME_tab2,END_TIME_tab2,))
		row = cur.fetchone()

		while row is not None:
			ch0.append(row["ch0"])
			ch1.append(row["ch1"])
			ch2.append(row["ch2"])
			ch3.append(row["ch3"])
			ch4.append(row["ch4"])
			ch5.append(row["ch5"])
			time_tab2.append(row["datetime"])
			row = cur.fetchone()


	db_gui.close()



	time_tab2_first = str(time_tab2[0])
	print("time_tab2_first=",time_tab2_first )
	time_tab2_last = str(time_tab2[-1])

	first_time_tab2 = datetime.datetime.strptime(time_tab2_first,'%Y-%m-%d %H:%M:%S')
	time_tab2_dt = []
	time_tab2_el_mins = []
	time_tab2_el = []

	time_tab1_first = str(time_tab1[0])
	print("time_tab1_first=",time_tab1_first )
	time_tab1_last = str(time_tab1[-1])

	first_time_tab1 = datetime.datetime.strptime(time_tab1_first,'%Y-%m-%d %H:%M:%S')
	time_tab1_dt = []
	time_tab1_el_mins = []
	time_tab1_el = []


	for t in time_tab2:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_tab2
		time_tab2_dt.append(datime)#.time)
		time_tab2_el.append(elapsed.total_seconds())
		time_tab2_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
	for t in time_tab1:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_tab1
		time_tab1_dt.append(datime)#.time)
		time_tab1_el.append(elapsed.total_seconds())
		time_tab1_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes






	time_tab1_el=np.array(time_tab1_el)
	time_tab2_el=np.array(time_tab2_el)


	fig, axs = plt.subplots(4,1, sharex=True)
	ax = axs[0]
	ax.plot(time_tab1_el_mins, A0, label = "tab1")
	ax.plot(time_tab2_el_mins, ch0, label = "tab2")
	ax.legend()
	ax.set_ylabel("Bob 2")
	ax = axs[1]
	ax.plot(time_tab1_el_mins, B0, label = "tab1")
	ax.plot(time_tab2_el_mins, ch1, label = "tab2")
	ax.legend()
	ax.set_ylabel("Alice 1")
	ax = axs[2]
	ax.plot(time_tab1_el_mins, C0)
	ax.set_ylabel("BS output 1")
	ax = axs[3]
	ax.plot(time_tab1_el_mins, D0)
	ax.set_ylabel("BS output 2")
	ax.set_xlabel("Elapsed time (min)")


	A0 = np.array(A0)
	B0 = np.array(B0)
	C0 = np.array(C0)
	D0 = np.array(D0)


	fig, axs = plt.subplots(4,1, sharex=True)
	ax = axs[0]
	ax.plot(time_tab2_el_mins[:-300], ch2[:-300])
	ax.set_ylabel("Twofolds")
	ax = axs[1]
	ax.plot(time_tab2_el_mins[:-300], ch3[:-300])
	ax.set_ylabel("Threefold (heralding on Alice 1)")
	ax = axs[1]
	ax.plot(time_tab2_el_mins[:-300], ch4[:-300])
	ax.set_ylabel("Threefold (heralding on Bob 2)")
	ax = axs[3]
	ax.plot(time_tab2_el_mins[:-300], ch5[:-300])


	ax.set_ylabel("Fourfold")
	ax.set_xlabel("Elapsed time (min)")

	ch2 = np.array(ch2)
	ch3 = np.array(ch3)
	ch4 = np.array(ch4)
	ch5 = np.array(ch5)

	half = len(ch2)//2

	two_fold_max = sum(ch2[:half-300])
	two_fold_min = sum(ch2[half:-300])
	three_fold_max_a = sum(ch3[:half-300])
	three_fold_min_a = sum(ch3[half:-300])
	three_fold_max_b = sum(ch4[:half-300])
	three_fold_min_b = sum(ch4[half:-300])
	four_fold_max = sum(ch5[:half-300])
	four_fold_min = sum(ch5[half:-300])

	two_fold_vis = 1 - two_fold_min/two_fold_max
	three_fold_vis_a = 1 - three_fold_min_a/three_fold_max_a
	three_fold_vis_b = 1 - three_fold_min_b/three_fold_max_b
	four_fold_vis = 1 - four_fold_min/four_fold_max

	print("Total Time: ",time_tab2_el_mins[-300])

	print("Two fold maximum counts :",two_fold_max)
	print("Two fold minimum counts :",two_fold_min)
	print("Two fold visilbility: ",two_fold_vis)
	print("Three fold heralding Alice maximum counts :",three_fold_max_a)
	print("Three fold heralding Alice minimum counts :",three_fold_min_a)
	print("Three fold heralding Alice visilbility: ",three_fold_vis_a)
	print("Three fold heralding Bob maximum counts :",three_fold_max_b)
	print("Three fold heralding Bob minimum counts :",three_fold_min_b)
	print("Three fold heralding Bob visilbility: ",three_fold_vis_b)
	print("Four fold maximum counts :",four_fold_max)
	print("Four fold minimum counts :",four_fold_min)
	print("four fold visilbility: ",four_fold_vis)


#
# 	boolArr = np.argwhere(B0<5200)
# 	print(len(boolArr))
#
# 	time_tab1_el_mins_moded = np.array([time_tab1_el_mins[i[0]] for i in boolArr])
# 	time_tab2_el_mins_moded = np.array([time_tab2_el_mins[i[0]] for i in boolArr])
#
# 	#time_tab1_el_mins_moded = np.where(A0<7000,A0,time_tab1_el_mins_moded)
# 	#time_tab2_el_mins_moded = np.where(A0<7000,A0,time_tab2_el_mins_moded)
# 	A0 = np.array([A0[i[0]] for i in boolArr])
# 	C0 = np.array([C0[i[0]] for i in boolArr])
# 	and2 = np.array([and2[i[0]] for i in boolArr])
# 	bsm1 = np.array([bsm1[i[0]] for i in boolArr])
# 	B0 = np.array([B0[i[0]] for i in boolArr])
#
# 	print(A0)
# 	print(B0)
#
# 	fig, axs = plt.subplots(5,1, sharex=True)
# 	ax = axs[0]
# 	ax.plot(time_tab1_el_mins_moded, A0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("A0")
# 	ax = axs[1]
# 	ax.plot(time_tab1_el_mins_moded, B0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("B0")
# 	ax = axs[2]
# 	ax.plot(time_tab1_el_mins_moded, C0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("C0")
# 	ax = axs[3]
# 	ax.plot(time_tab2_el_mins_moded, and2)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("and2")
# 	ax = axs[4]
# 	ax.plot(time_tab2_el_mins_moded, bsm1)
# 	ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("bsm1")
# 	plt.show()
#
# 	max_two_fold = np.sum(and2)
# 	max_three_fold = np.sum(bsm1)
#
# 	max_two_fold_norm = np.sum(and2/B0)*np.mean(B0)
# 	max_three_fold_norm = np.sum(bsm1/B0)*np.mean(B0)
#
# 	rb_max = np.mean(B0)
# 	rc_max = np.mean(C0)
#
# 	time_max = len(B0)
#
# 	print("------Non-Normalized Max Counts------")
# 	print("Two Fold {}".format(max_two_fold))
# 	print("Three Fold {}".format(max_three_fold))
# 	print("------Normalized Max Counts------")
# 	print("Two Fold {}".format(max_two_fold_norm))
# 	print("Three Fold {}".format(max_three_fold_norm))
#
#
# except KeyboardInterrupt:
#  	print("Quit")
#
#
# START_TIME = '2022-04-05 14:24:00'
# END_TIME = '2022-04-05 15:40:00'
#
# #START_TIME = '2019-12-11 12:14:00'
# #END_TIME = '2019-12-11 14:47:54'
#
#
# #connect to database
#
#
# and1=[]
# bufferand1=[]
# bufferand2=[]
# bufferand3=[]
# and2 = []
# and3 = []
# or_gate = []
# bufferor_gate=[]
# bsm1 = []
# bufferbsm1=[]
# bsm2 = []
# bufferbsm2=[]
#
# A0=[]
# B0=[]
# C0=[]
# A1=[]
# B1=[]
# C1=[]
# A2=[]
# B2=[]
# C2=[]
# time_tab2=[]
# time_tab1=[]
#
# T_Vap = []
# T_Vin = []
#
# min_two_fold = 0
# min_two_fold_norm = 0
#
# min_three_fold = 0
# min_three_fold_norm = 0
#
# rc_min = 0
#
# try:
# 	db_gui = pymysql.connect(host="192.168.2.3",
# 						 user="GUI2",
# 						 passwd="Teleport1536!",  # your password
# 						 db="INQNET_GUI")
# 						 #charset='utf8mb4')
# 	with db_gui.cursor(pymysql.cursors.DictCursor) as cur:
# 		TABLE_NAME = "inqnet_gui_tab2gates_V3"
# 		queryGUI = "SELECT and1, and2, and3,orgate, bsm1, bsm2, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
# 		cur.execute(queryGUI, (START_TIME,END_TIME,))
# 		row = cur.fetchone()
#
# 		while row is not None:
#
# 			and1.append(row["and1"])
# 			and2.append(row["and2"])
# 			and3.append(row["and3"])
# 			bsm1.append(row["bsm1"])
# 			bsm2.append(row["bsm2"])
# 			or_gate.append(row["orgate"])
# 			time_tab2.append(row["datetime"])
# 			#print
# 			row = cur.fetchone()
#
# 		TABLE_NAME = "inqnet_gui_historates"
# 		queryGUI = "SELECT A0, B0, C0, A1, B1, C1, A2, B2,C2, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
# 		cur.execute(queryGUI, (START_TIME,END_TIME,))
# 		row = cur.fetchone()
# 		while row is not None:
# 			A0.append(row["A0"])
# 			B0.append(row["B0"])
# 			C0.append(row["C0"])
# 			A1.append(row["A1"])
# 			B1.append(row["B1"])
# 			C1.append(row["C1"])
# 			A2.append(row["A2"])
# 			B2.append(row["B2"])
# 			C2.append(row["C2"])
# 			time_tab1.append(row["datetime"])
# 			row = cur.fetchone()
# 	db_gui.close()
#
#
#
# 	time_tab2_first = str(time_tab2[0])
# 	print("time_tab2_first=",time_tab2_first )
# 	time_tab2_last = str(time_tab2[-1])
#
# 	first_time_tab2 = datetime.datetime.strptime(time_tab2_first,'%Y-%m-%d %H:%M:%S')
# 	time_tab2_dt = []
# 	time_tab2_el_mins = []
# 	time_tab2_el = []
#
# 	time_tab1_first = str(time_tab1[0])
# 	print("time_tab1_first=",time_tab1_first )
# 	time_tab1_last = str(time_tab1[-1])
#
# 	first_time_tab1 = datetime.datetime.strptime(time_tab1_first,'%Y-%m-%d %H:%M:%S')
# 	time_tab1_dt = []
# 	time_tab1_el_mins = []
# 	time_tab1_el = []
#
#
# 	for t in time_tab2:
# 		t=str(t)
# 		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
# 		elapsed = datime - first_time_tab2
# 		time_tab2_dt.append(datime)#.time)
# 		time_tab2_el.append(elapsed.total_seconds())
# 		time_tab2_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
# 	for t in time_tab1:
# 		t=str(t)
# 		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
# 		elapsed = datime - first_time_tab1
# 		time_tab1_dt.append(datime)#.time)
# 		time_tab1_el.append(elapsed.total_seconds())
# 		time_tab1_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes
#
#
#
#
#
#
# 	time_tab1_el=np.array(time_tab1_el)
# 	time_tab2_el=np.array(time_tab2_el)
#
#
# 	fig, axs = plt.subplots(5,1, sharex=True)
# 	ax = axs[0]
# 	ax.plot(time_tab1_el_mins, A0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("A0")
# 	ax = axs[1]
# 	ax.plot(time_tab1_el_mins, B0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("B0")
# 	ax = axs[2]
# 	ax.plot(time_tab1_el_mins, C0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("C0")
# 	ax = axs[3]
# 	ax.plot(time_tab2_el_mins, and2)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("and2")
# 	ax = axs[4]
# 	ax.plot(time_tab2_el_mins, bsm1)
# 	ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("bsm1")
# 	plt.show()
#
# 	A0 = np.array(A0)
# 	B0 = np.array(B0)
# 	C0 = np.array(C0)
# 	and2 = np.array(and2)
#
# 	boolArr = np.argwhere(B0<5200)
# 	print(len(boolArr))
#
# 	time_tab1_el_mins_moded = np.array([time_tab1_el_mins[i[0]] for i in boolArr])
# 	time_tab2_el_mins_moded = np.array([time_tab2_el_mins[i[0]] for i in boolArr])
#
# 	#time_tab1_el_mins_moded = np.where(A0<7000,A0,time_tab1_el_mins_moded)
# 	#time_tab2_el_mins_moded = np.where(A0<7000,A0,time_tab2_el_mins_moded)
# 	A0 = np.array([A0[i[0]] for i in boolArr])
# 	C0 = np.array([C0[i[0]] for i in boolArr])
# 	and2 = np.array([and2[i[0]] for i in boolArr])
# 	bsm1 = np.array([bsm1[i[0]] for i in boolArr])
# 	B0 = np.array([B0[i[0]] for i in boolArr])
#
# 	print(A0)
# 	print(B0)
#
# 	fig, axs = plt.subplots(5,1, sharex=True)
# 	ax = axs[0]
# 	ax.plot(time_tab1_el_mins_moded, A0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("A0")
# 	ax = axs[1]
# 	ax.plot(time_tab1_el_mins_moded, B0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("B0")
# 	ax = axs[2]
# 	ax.plot(time_tab1_el_mins_moded, C0)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("C0")
# 	ax = axs[3]
# 	ax.plot(time_tab2_el_mins_moded, and2)
# 	#ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("and2")
# 	ax = axs[4]
# 	ax.plot(time_tab2_el_mins_moded, bsm1)
# 	ax.set_xlabel("Elapsed time (min)")
# 	ax.set_ylabel("bsm1")

#
# 	min_two_fold = np.sum(and2)
# 	min_three_fold = np.sum(bsm1)
#
# 	min_two_fold_norm = np.sum(and2/B0)*np.mean(B0)
# 	min_three_fold_norm = np.sum(bsm1/B0)*np.mean(B0)
#
# 	rb_min = np.mean(B0)
# 	rc_min = np.mean(C0)
#
# 	rc_scaling = rc_max/rc_min
# 	rb_scaling = rb_max/rb_min
#
# 	time_min = len(B0)
#
# 	time_scaling = time_min/time_max
#
#
#
# 	print("------Non-Normalized Min Counts------")
# 	print("Two Fold {}".format(min_two_fold))
# 	print("Three Fold {}".format(min_three_fold))
# 	print("------Normalized Min Counts------")
# 	print("Two Fold {}".format(min_two_fold_norm))
# 	print("Three Fold {}".format(min_three_fold_norm))
#
# 	print("\n")
#
#
#
# 	print("------Non-Normalized------")
# 	print("-----Two-Fold HOM Visibility-----")
# 	print(1-min_two_fold/(max_two_fold*time_scaling))
# 	print("-----Three-Fold HOM Visibility-----")
# 	print(1-min_three_fold/(max_three_fold*time_scaling))
#
# 	print("------Rc Normalized------")
# 	print("-----Two-Fold HOM Visibility-----")
# 	print(1-min_two_fold*rc_scaling/(max_two_fold*time_scaling))
# 	print("-----Three-Fold HOM Visibility-----")
# 	print(1-min_three_fold*rc_scaling/(max_three_fold*time_scaling))
#
# 	print("------Rb Normalized Element------")
# 	print("-----Two-Fold HOM Visibility-----")
# 	print(1-min_two_fold_norm/(max_two_fold_norm*time_scaling))
# 	print("-----Three-Fold HOM Visibility-----")
# 	print(1-min_three_fold_norm/(max_three_fold_norm*time_scaling))
#
# 	print("------Rb Normalized Mean------")
# 	print("-----Two-Fold HOM Visibility-----")
# 	print(1-min_two_fold*rb_scaling/(max_two_fold*time_scaling))
# 	print("-----Three-Fold HOM Visibility-----")
# 	print(1-min_three_fold*rb_scaling/(max_three_fold*time_scaling))

	plt.show()
except KeyboardInterrupt:
	print("Quit")
