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

	IM_pulse_data = np.load('Bob_new_IM_min_max_data_wide_pulse.npy')
	IM_min = [float(data[:-1])*1e3 for data in IM_pulse_data[0]]
	IM_max = [float(data[:-1])*1e3 for data in IM_pulse_data[1] if float(data[:-1]) < 1]

	bias_mon = np.loadtxt('IM_POM/Bob_new_IM_input_power_wide_pulse.csv',skiprows=15,delimiter=',',dtype='S')
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

	fig1, axs = plt.subplots(3,1, num=238, sharex = True)
	# xmin=time_Vap_el_mins[0] #40
	# xmax=time_Vap_el_mins[-1] #60

	#histo_indices = np.where(time_histo_el_mins > time_Vap_el_mins[0])
	#histo_indices = histo_indices[0]


	histo_indices= range(1,len(time_POM_el))

	tab1_data = [IM_max,IM_min,bias_voltage[1:]]#, [Rb1, Rb2, Rb3], [Rc1, Rc2, Rc3]]
	tab1_titles = ["IM Max amplitude (mV)", "IM Min amplitude (mV)", "Input Power"]#, ["Rb1", "Rb2", "Rb3"], ["Rc1","Rc2", "Rc3"]]

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

	for i in range(3):
		#for j in range(1):
		axs[i].plot(tab1_data[i],  linestyle = 'none', marker= '.', markersize=8)
		axs[i].set_ylabel(tab1_titles[i])
	axs[2].set_xlabel('Elapsed time (s)', fontsize =16)



	##Saving Counts Plots into Disk
	fig1.savefig('counts_noise_signal.png')
	fig1.savefig('counts_noise_signal.pdf')
	plt.show()






except KeyboardInterrupt:
	print("Quit")
