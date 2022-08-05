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
#delay_step_times = np.array([5,5,5,5,5,5,5,5,5,5,5,5,5,5,5])*4*60##how many seconds per step(10 minutes is 600)
adqtime_tab1=1
adqtime_tab2=1
adqtime_histo=1


#START_TIME = '2022-05-24 21:46:00'
#END_TIME = '2022-05-25	00:06:30'

#START_TIME = '2019-12-11 12:14:00'
#END_TIME = '2019-12-11 14:47:54'


#connect to database



A0,A1,A2 = [],[],[]
B0,B1,B2=[],[],[]
C0,C1,C2=[],[],[]
D0,D1,D2 = [],[],[]

# Ch0 → Alice and Rate
# Ch1 → Bob and Rate
# Ch2 → 2 fold HOM
# Ch3 → 3 fold HOM Alice Heralding
# Ch4 → 3 fold HOM Bob Heralding
# Ch5 → 4 fold HOM
# Ch6 → Alice or Rate
# Ch7 → Bob or Rate


Ch0,Ch1 =[],[]

WLA1, WLA2, WLB1, WLB2 = [],[],[],[]
BWA1,BWA2,BWB1,BWB2 = [],[],[],[]


time_JSI,time_tab1,time_tab2=[],[],[]



max_two_fold = 0
max_two_fold_norm = 0

max_three_fold = 0
max_three_fold_norm = 0

rc_max = 0

try:
	db_gui = pymysql.connect(host="192.168.2.3",
						 user="GUI3",
						 passwd="Teleport1536!",  # your password
						 db="INQNET_GUI")
						 #charset='utf8mb4')
	with db_gui.cursor(pymysql.cursors.DictCursor) as cur:
		TABLE_NAME = "ExfoJSI_1"
		queryFILTER = "SELECT * FROM "+TABLE_NAME
		cur.execute(queryFILTER)
		row = cur.fetchone()
		while row is not None:
			WLA1.append(row["wavelengthA1"])
			WLA2.append(row["wavelengthA2"])
			WLB1.append(row["wavelengthB1"])
			WLB2.append(row["wavelengthB2"])
			BWA1.append(row["bandwidthA1"])
			BWA2.append(row["bandwidthA2"])
			BWB1.append(row["bandwidthB1"])
			BWB2.append(row["bandwidthB2"])
			time_JSI.append(row["datetime"])
			row = cur.fetchone()

		START_TIME = str(time_JSI[0])
		SECOND_TIME = str(time_JSI[1])
		delta_time =  datetime.datetime.strptime(SECOND_TIME,'%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(START_TIME,'%Y-%m-%d %H:%M:%S')
		END_TIME = time_JSI[-1]
		END_TIME = END_TIME + datetime.timedelta(seconds=delta_time.total_seconds())




		TABLE_NAME = "TAB125_05_2022_16_21_20"
		queryGUI = "SELECT A0, A1, A2, B0, B1, B2, C0, C1, C2,D0, D1, D2, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
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


		TABLE_NAME = "TAB225_05_2022_16_21_20"
		queryGUI = "SELECT ch0, ch1, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()

		while row is not None:
			Ch0.append(row["ch0"])
			Ch1.append(row["ch1"])
			time_tab2.append(row["datetime"])
			row = cur.fetchone()


	db_gui.close()

	#print(time_tab2)

	#Find the time of integration of each filter setting

	first_time_JSI = datetime.datetime.strptime(str(time_JSI[0]),'%Y-%m-%d %H:%M:%S')
	second_time_JSI = datetime.datetime.strptime(str(time_JSI[1]),'%Y-%m-%d %H:%M:%S')

	delta_time = second_time_JSI - first_time_JSI
	delta_time = delta_time.total_seconds()



	time_tab2_first = str(time_tab2[0])
	print("time_tab2_first=",time_tab2_first )
	time_tab2_last = str(time_tab2[-1])

	print(time_tab2_last)

	first_time_tab2 = datetime.datetime.strptime(time_tab2_first,'%Y-%m-%d %H:%M:%S')
	time_tab2_dt = []
	time_tab2_el_mins = []
	time_tab2_el = []

	time_histo_first = str(time_tab1[0])
	print("time_histo_first=",time_histo_first )
	time_histo_last = str(time_tab1[-1])
	print("time_histo_last=",time_histo_last )

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
	for t in time_tab1:
		t=str(t)
		datime=datetime.datetime.strptime(t,'%Y-%m-%d %H:%M:%S')
		elapsed = datime - first_time_histo
		time_histo_dt.append(datime)#.time)
		time_histo_el.append(elapsed.total_seconds())
		time_histo_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes






	time_histo_el=np.array(time_histo_el)
	time_tab2_el=np.array(time_tab2_el)

	print("time_tab2_el: ",time_tab2_el[-1])



	cur_file_base = os.path.basename(__file__)
	cur_file_name = os.path.splitext(cur_file_base)[0]
	csv_filename_histo= cur_file_name+"_histo.csv"
	csv_filename_tab2= cur_file_name+"_tab2.csv"
	path_to_file ="/home/fqnet/Software/FQNET/FQNET_HOM_2022April/"
	df_histo =pd.DataFrame(list(zip(time_histo_el, A0, A1, A2, B0, B1, B2, C0, C1, C2, D0, D1, D2)))
	df_histo.columns=["time_histo_el_s", "A0", "A1", "A2", "B0", "B1", "B2", "C0", "C1", "C2", "D0", "D1", "D2"]
	df_histo.to_csv(path_to_file+csv_filename_histo)

	df_tab2 =pd.DataFrame(list(zip(time_tab2_el, Ch0, Ch1)))
	df_tab2.columns=["time_histo_el_s", "ch0", "ch1"]
	df_tab2.to_csv(path_to_file+csv_filename_tab2)

	time_histo_el_bin = []
	time_tab2_el_bin = []
	a0_bin = []
	a1_bin = []
	a2_bin = []
	b0_bin = []
	b1_bin = []
	b2_bin = []
	c0_bin = []
	c1_bin = []
	c2_bin = []
	d0_bin = []
	d1_bin = []
	d2_bin = []
	ch0_bin = []
	ch1_bin = []


	a0 = 0
	a1 = 0
	a2 = 0
	b0 = 0
	b1 = 0
	b2 = 0
	c0 = 0
	c1 = 0
	c2 = 0
	d0 = 0
	d1 = 0
	d2 = 0
	ch0 = 0
	ch1 = 0

	j=0

	print("I's length:", len(time_tab2_el))

	for i in range(len(time_tab2_el)):
		ch0 = ch0 + Ch0[i]
		ch1 = ch1 + Ch1[i]
		#print(adqtime/10)
		if i%round(delta_time/adqtime_tab2)==0:
			#print(time_tab2_el[i]
			time_tab2_el_bin.append(round(time_tab2_el[i]))
			ch0_bin.append(ch0)
			ch1_bin.append(ch1)
			# dlh = time_histo_el[i]
			# dltab2 = time_tab2_el[i]
			#print(and2_bin)
			ch0 = Ch0[i]
			ch1 = Ch1[i]





	#print("After binning for loop")
	#print(bsm1_bin)
	j=0
	for i in range(len(time_histo_el)):
		a0 = a0 + A0[i]
		a1 = a1 + A1[i]
		a2 = a2 + A2[i]
		b0 = b0 + B0[i]
		b1 = b1 + B1[i]
		b2 = b2 + B2[i]
		c0 = c0 + C0[i]
		c1 = c1 + C1[i]
		c2 = c2 + C2[i]
		d0 = d0 + D0[i]
		d1 = d1 + D1[i]
		d2 = d2 + D2[i]
		if i%round(delta_time/adqtime_histo)==0:
			#print(time_histo_el[i])
			time_histo_el_bin.append(round(time_histo_el[i]))
			a0_bin.append(a0)
			a1_bin.append(a1)
			a2_bin.append(a2)
			b0_bin.append(b0)
			b1_bin.append(b1)
			b2_bin.append(b2)
			c0_bin.append(c0)
			c1_bin.append(c1)
			c2_bin.append(c2)
			d0_bin.append(d0)
			d1_bin.append(d1)
			d2_bin.append(d2)
			a0 = A0[i]
			a1 = A1[i]
			a2 = A2[i]
			b0 = B0[i]
			b1 = B1[i]
			b2 = B2[i]
			c0 = C0[i]
			c1 = C1[i]
			c2 = C2[i]
			d0 = D0[i]
			d1 = D1[i]
			d2 = D2[i]



   #print(time_histo_el)
       #print(time_tab2_el)

    #histo_indices = np.where(time_histo_el > time_tab2_el[0])
   #histo_indices = histo_indices[0]

       #time_histo_el = time_histo_el[histo_indices[0]:histo_indices[-1]]

  #Ra1 = Ra1[histo_indices[0]:histo_indices[-1]]
 #Rb1 = Rb1[histo_indices[0]:histo_indices[-1]]
        #Rc1 = Rc1[histo_indices[0]:histo_indices[-1]]






	#Stacked plot of all data

	fig1, axs = plt.subplots(4,1, num=238, sharex = True)
	# xmin=time_Vap_el_mins[0] #40
	# xmax=time_Vap_el_mins[-1] #60

	#histo_indices = np.where(time_histo_el_mins > time_Vap_el_mins[0])
	#histo_indices = histo_indices[0]


	histo_indices= range(1,len(time_histo_el))

	tab1_data = [A0, B0, C0, D0]#, [Rb1, Rb2, Rb3], [Rc1, Rc2, Rc3]]
	tab1_titles = ["Alice 1", "Bob 1", "Bob 2", "Alice 2"]#, ["Rb1", "Rb2", "Rb3"], ["Rc1","Rc2", "Rc3"]]

	print(len(histo_indices), 'len histo indicies')

	# NEW_time_histo_el_mins=[]
	# print(time_histo_el_mins, 'histo')
	# for a in range(0,len(time_histo_el_mins)):
	# 	NEW_time_histo_el_mins.append(round(time_histo_el_mins[a]))
	# print(len(tab1_data[1]), 'tabl_data len')
	# #[len(a) for a in my_tuple_2d]
	#meanCounts=np.mean(Rc1_bin)
	#normRA1Array= np.array(Ra1_bin)/meanCounts
	#normRB1Array= np.array(Rb1_bin)/meanCounts
	#normRC1Array= np.array(Rc1_bin)/meanCounts
        #print(len(Ra1_bin), len(and1_bin), 'RA1 len', 'and1bin len' )
        #print(meanCounts)

	for i in range(4):
		#for j in range(1):
		axs[i].plot(time_histo_el[histo_indices[0]:histo_indices[-1]], tab1_data[i][histo_indices[0]:histo_indices[-1]],  linestyle = 'none', marker= '.', markersize=8)
		axs[i].set_ylabel(tab1_titles[i])
		#if i==1 or i == 3:
		#	axs[i].vlines(time_histo_el_bin,100000,150000,color='r')
		#else:
			#axs[i].vlines(time_histo_el_bin,4000,8000,color='r')
	axs[3].set_xlabel('Elapsed time (s)', fontsize =16)



	##Saving Counts Plots into Disk
	fig1.savefig('counts_4f.png')
	fig1.savefig('counts_4f.pdf')
	plt.show()

	min_wl = min(WLA1)
	max_wl = max(WLA1)
	delta_wl = BWA1[0]


	y,x = np.mgrid[min_wl:max_wl+delta_wl:delta_wl, min_wl:max_wl+delta_wl:delta_wl]

	Alice_JSI = np.array(ch0_bin[0:6561]).reshape(81,81)
	Bob_JSI = np.array(ch1_bin[0:6561]).reshape(81,81)

	print(min_wl)
	print(max_wl)
	print(delta_wl)

	fig1,axs1 = plt.subplots(1,2, num=300)
	ax = axs1[0]


	c = ax.pcolormesh(x,y,Alice_JSI)
	ax.set_title("Alice")
	fig1.colorbar(c, ax=ax)

	ax = axs1[1]


	c = ax.pcolormesh(x,y,Bob_JSI)
	ax.set_title("Bob")
	fig1.colorbar(c, ax=ax)

	plt.show()






except KeyboardInterrupt:
	print("Quit")
