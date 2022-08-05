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
delay_step_times = np.array([60,60,60,90,90,90,90,90,90,90,90,90,60,60,60])*60##how many seconds per step(10 minutes is 600)
adqtime_tab2=2
adqtime_histo=2


START_TIME = '2022-04-20 16:57:00'
END_TIME = '2022-04-20	17:02:00'

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


Ch0,Ch1,Ch2,Ch3,Ch4,Ch5,Ch6,Ch7,Ch8,Ch9,Ch10 =[],[],[],[],[],[],[],[],[],[],[]


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
		TABLE_NAME = "TAB119_04_2022_13_46_43"
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


		TABLE_NAME = "TAB219_04_2022_13_46_43"
		queryGUI = "SELECT ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()

		while row is not None:
			Ch0.append(row["ch0"])
			Ch1.append(row["ch1"])
			Ch2.append(row["ch2"])
			Ch3.append(row["ch3"])
			Ch4.append(row["ch4"])
			Ch5.append(row["ch5"])
			Ch6.append(row["ch6"])
			Ch7.append(row["ch7"])
			Ch8.append(row["ch8"])
			Ch9.append(row["ch9"])
			Ch10.append(row["ch10"])
			time_tab2.append(row["datetime"])
			row = cur.fetchone()


	db_gui.close()

	print(time_tab1)



	time_tab2_first = str(time_tab2[0])
	print("time_tab2_first=",time_tab2_first )
	time_tab2_last = str(time_tab2[-1])

	#print(time_tab2_last)

	first_time_tab2 = datetime.datetime.strptime(time_tab2_first,'%Y-%m-%d %H:%M:%S')
	time_tab2_dt = []
	time_tab2_el_mins = []
	time_tab2_el = []

	time_histo_first = str(time_tab1[0])
	print("time_histo_first=",time_histo_first )
	time_histo_last = str(time_tab1[-1])

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

	df_tab2 =pd.DataFrame(list(zip(time_tab2_el, Ch0, Ch1, Ch2, Ch3, Ch4, Ch5, Ch6, Ch7, Ch8, Ch9, Ch10)))
	df_tab2.columns=["time_histo_el_s", "ch0", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9", "ch10"]
	df_tab2.to_csv(path_to_file+csv_filename_tab2)

	bias_mon = np.loadtxt('IM_POM/IM_30G_20A_1400D.csv',skiprows=15,delimiter=',',dtype='S')
	bias_time = [b[2] for b in bias_mon]
	bias_voltage = [float(b[-1]) for b in bias_mon]
	print(bias_time)
	print(bias_voltage)

	time_POM_first = bias_time[0][1:].decode('UTF-8')
	#print(bias_time[0].dtype)
	print("time_POM_first=",time_POM_first )
	time_POM_last = bias_time[-1][1:].decode('UTF-8')

	#print(time_tab2_last)

	first_time_POM = datetime.datetime.strptime(time_POM_first,'%H:%M:%S.%f')
	time_POM_dt = []
	time_POM_el_mins = []
	time_POM_el = []

	for t in bias_time:
		t = t[1:].decode('UTF-8')
		datime=datetime.datetime.strptime(t,'%H:%M:%S.%f')
		elapsed = datime - first_time_POM
		time_POM_dt.append(datime)#.time)
		time_POM_el.append(elapsed.total_seconds())
		time_POM_el_mins.append((elapsed.total_seconds())/60) #Convert elapsed time from seconds to minutes





	#Stacked plot of all data

	fig1, axs = plt.subplots(4,1, num=238, sharex = True)
	# xmin=time_Vap_el_mins[0] #40
	# xmax=time_Vap_el_mins[-1] #60

	#histo_indices = np.where(time_histo_el_mins > time_Vap_el_mins[0])
	#histo_indices = histo_indices[0]


	histo_indices= range(1,len(time_tab2_el))

	tab1_data = [Ch7, Ch8, Ch9, Ch10]#, [Rb1, Rb2, Rb3], [Rc1, Rc2, Rc3]]
	tab1_titles = ["total ee ll", "total el le", "noise", "signal"]#, ["Rb1", "Rb2", "Rb3"], ["Rc1","Rc2", "Rc3"]]

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
		axs[i].plot(time_tab2_el[histo_indices[0]:histo_indices[-1]], tab1_data[i][histo_indices[0]:histo_indices[-1]],  linestyle = 'none', marker= '.', markersize=8)
		axs[i].set_ylabel(tab1_titles[i])
	axs[3].set_xlabel('Elapsed time (s)', fontsize =16)



	##Saving Counts Plots into Disk
	fig1.savefig('counts_noise_signal.png')
	fig1.savefig('counts_noise_signal.pdf')
	plt.show()


	fig2, axs2 = plt.subplots(5,1, num=300, sharex = True)



	tab2_data = [A0, B0, C0, D0]#, [Rb1, Rb2, Rb3], [Rc1, Rc2, Rc3]]
	tab2_titles = ["Counts A", "Counts B", "Counts C", "Counts D"]#, ["Rb1", "Rb2", "Rb3"], ["Rc1","Rc2", "Rc3"]]

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
		axs2[i].plot(time_histo_el[histo_indices[0]:histo_indices[-1]], tab2_data[i][histo_indices[0]:histo_indices[-1]],  linestyle = 'none', marker= '.', markersize=8)
		axs2[i].set_ylabel(tab2_titles[i])
	axs2[4].plot(time_POM_el,bias_voltage)
	axs2[4].set_ylabel('Power (W)')
	axs2[4].set_xlabel('Elapsed time (s)', fontsize =16)



	##Saving Counts Plots into Disk
	#fig1.savefig('counts_noise_signal.png')
	#fig1.savefig('counts_noise_signal.pdf')
	plt.show()

	fig3, axs3 = plt.subplots(2,1, num=300, sharex = True)

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


	axs3[0].plot(time_histo_el[histo_indices[0]:histo_indices[-1]], tab2_data[1][histo_indices[0]:histo_indices[-1]],  linestyle = '-', marker= '.', markersize=8)
	axs3[0].set_ylabel(tab2_titles[1])
	axs3[1].plot(time_POM_el,bias_voltage)
	axs3[1].set_ylabel('Power (W)')
	axs3[1].set_xlabel('Elapsed time (s)', fontsize =16)

	plt.show()

	ee_counts = sum(Ch3)
	ll_counts = sum(Ch4)
	el_counts = sum(Ch5)
	le_counts = sum(Ch6)

	noise = sum(Ch9)
	signal = sum(Ch10)

	BSM = sum(Ch2)

	#total_noise = ee_noise + ll_noise
	#total_signal = el_signal + le_signal


	fidelity = signal/(signal+noise)


	print("signal counts: ",signal)
	print("noise counts: ",noise)

	print("Swapping Fidelity: ",fidelity)

	print("BSMs: ",BSM)






except KeyboardInterrupt:
	print("Quit")
