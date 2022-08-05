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
adqtime_histo=2


START_TIME = '2022-07-27 14:35:26'
END_TIME = '2022-07-28 03:25:30'
table_start_time = "26_07_2022_16_11_29"
tab1_table_name = "TAB1"+table_start_time
tab2_table_name = "TAB2"+table_start_time
print(tab1_table_name)
print(tab2_table_name)

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


Ch0,Ch1,Ch2,Ch3,Ch4,Ch5,Ch6,Ch7,Ch8,Ch9,Ch10,Ch11,Ch12,Ch13,Ch14,Ch15,Ch16 =[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]


time_tab1,time_tab2=[],[]



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
		TABLE_NAME = tab1_table_name
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


		TABLE_NAME = tab2_table_name
		queryGUI = "SELECT ch0, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8, ch9, ch10, ch11, ch12, ch13, ch14, ch15, ch16, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
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
			Ch11.append(row["ch11"])
			Ch12.append(row["ch12"])
			Ch13.append(row["ch13"])
			Ch14.append(row["ch14"])
			Ch15.append(row["ch15"])
			Ch16.append(row["ch16"])
			time_tab2.append(row["datetime"])
			row = cur.fetchone()


	db_gui.close()

	print(time_tab2)



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
	csv_filename_tab1= cur_file_name+"_tab1.csv"
	csv_filename_tab2= cur_file_name+"_tab2.csv"
	path_to_file ="/home/fqnet/Software/FQNET/FQNET_2022April/SWAP"
	df_tab1 =pd.DataFrame(list(zip(time_histo_el, A0, A1, A2, B0, B1, B2, C0, C1, C2, D0, D1, D2)))
	df_tab1.columns=["time_histo_el_s", "A0", "A1", "A2", "B0", "B1", "B2", "C0", "C1", "C2", "D0", "D1", "D2"]
	df_tab1.to_csv(path_to_file+csv_filename_tab2)

	df_tab1 =pd.DataFrame(list(zip(time_tab2_el, Ch0, Ch1, Ch2, Ch3, Ch4, Ch5, Ch6, Ch7, Ch8, Ch9, Ch10, Ch11, Ch12, Ch13, Ch14, Ch15, Ch16)))
	df_tab1.columns=["time_histo_el_s", "ch0", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9", "ch10", "ch11", "ch12", "ch13", "ch14", "ch15", "ch16"]
	df_tab1.to_csv(path_to_file+csv_filename_tab1)

	x_basis_signal = []
	x_basis_noise = []
	x_basis_signal_1 = []
	x_basis_noise_1 = []

	bin = 0
	bin_1 = 0

	j=0

	for i in range(len(time_tab2_el)):
		bin = bin+Ch15[i]
		bin_1 = bin_1+Ch16[i]
		#print(adqtime/10)
		if  i%round(5*60/adqtime_tab2)==0:
			#print(time_tab2_el[i]
			if j%2==1:
				x_basis_noise.append(bin)
				x_basis_signal_1.append(bin_1)
			else:
				x_basis_signal.append(bin)
				x_basis_noise_1.append(bin_1)
			bin = Ch15[i]
			bin_1 = Ch16[i]
			j=j+1




	####################
	#### TAB 1 DATA ####
	####################
	tab1_indices = range(len(time_histo_el))
	fig1, axs1 = plt.subplots(4,3, sharex = True)
	tab1_data = [[A0, A1, A2], [B0, B1, B2], [C0, C1, C2], [D0, D1, D2]]
	tab1_titles = [["A0", "A1", "A2"], ["B0", "B1", "B2"], ["C0", "C1", "C2"], ["D0", "D1", "D2"]]

	for j in range(3):
		for i in range(4):
			axs1[i][j].plot(time_histo_el[tab1_indices[0]:tab1_indices[-1]], tab1_data[i][j][tab1_indices[0]:tab1_indices[-1]],  linestyle = 'none', marker= '.', markersize=8)
			axs1[i][j].set_ylabel(tab1_titles[i][j])
		axs1[i][j].set_xlabel('Elapsed time (s)', fontsize =16)

	plt.tight_layout()
	##Saving Counts Plots into Disk
	figname = 'singles_{}'.format(table_start_time)
	fig1.savefig(figname+".png")
	fig1.savefig(figname+".pdf")
	plt.show()



	####################
	#### TAB 2 DATA ####
	####################

	fig2, axs2 = plt.subplots(1,1, num=238, sharex = True)
	tab2_indices= range(len(time_tab2_el))
	tab2_data = [Ch6]#, [Rb1, Rb2, Rb3], [Rc1, Rc2, Rc3]]
	tab2_titles = ["BSM"]#, ["Rb1", "Rb2", "Rb3"], ["Rc1","Rc2", "Rc3"]]

	for i in range(len(tab2_titles)):
		axs2.plot(time_tab2_el[tab2_indices[0]:tab2_indices[-1]], tab2_data[i][tab2_indices[0]:tab2_indices[-1]],  linestyle = 'none', marker= '.', markersize=8)
		axs2.set_ylabel(tab2_titles[i])
	axs2.set_xlabel('Elapsed time (s)', fontsize =16)

	##Saving Counts Plots into Disk
	figname = 'zbasis_{}'.format(table_start_time)
	fig2.savefig(figname+".png")
	fig2.savefig(figname+".pdf")
	plt.show()

	plt.plot(x_basis_signal, linestyle = 'none', marker= '.', markersize=8, label='signal')
	plt.plot(x_basis_noise, linestyle = 'none', marker= '.', markersize=8, label='noise')

	plt.legend()

	plt.show()

	plt.plot(x_basis_signal_1, linestyle = 'none', marker= '.', markersize=8, label='signal')
	plt.plot(x_basis_noise_1, linestyle = 'none', marker= '.', markersize=8, label='noise')

	plt.legend()

	plt.show()


	####################
	#### FIDELITIES ####
	####################

	#ee_counts = sum(Ch9)
	#ll_counts = sum(Ch10)
	#el_counts = sum(Ch7)
	#le_counts = sum(Ch8)

	#noise = sum(Ch14) # z basis fail
	#signal = sum(Ch13) # z basis succes

	#x_basis_signal = sum(Ch16)

	BSM = sum(Ch6)




	#fidelity = signal/(signal+noise)
	#error_n = np.sqrt(noise)*signal/((signal+noise)**2)
	#error_s = np.sqrt(signal)*noise/((signal+noise)**2)
	#total_error = np.sqrt(error_n**2+error_s**2)

	x_basis_signal = sum(x_basis_signal)
	x_basis_noise = sum(x_basis_noise)
	x_basis_signal_1 = sum(x_basis_signal_1)
	x_basis_noise_1 = sum(x_basis_noise_1)

	fidelity_x = x_basis_signal/(x_basis_signal+x_basis_noise)
	error_n_x = np.sqrt(x_basis_noise)*x_basis_signal/((x_basis_signal+x_basis_noise)**2)
	error_s_x = np.sqrt(x_basis_signal)*x_basis_noise/((x_basis_signal+x_basis_noise)**2)
	total_error_x = np.sqrt(error_n_x**2+error_s_x**2)

	fidelity_x_1 = x_basis_signal_1/(x_basis_signal_1+x_basis_noise_1)
	error_n_x_1 = np.sqrt(x_basis_noise_1)*x_basis_signal_1/((x_basis_signal_1+x_basis_noise_1)**2)
	error_s_x_1 = np.sqrt(x_basis_signal_1)*x_basis_noise_1/((x_basis_signal_1+x_basis_noise_1)**2)
	total_error_x_1 = np.sqrt(error_n_x_1**2+error_s_x_1**2)

	alice_signal = sum(Ch0)
	alice_noise = sum(Ch1)

	bob_signal = sum(Ch2)
	bob_noise = sum(Ch3)


	#print("signal counts: ",signal)
	#print("noise counts: ",noise)

	#print("Swapping Fidelity: ",fidelity)
	#print("Swapping Error: ",total_error)

	print("x signal counts: ",x_basis_signal)
	print("x noise counts: ",x_basis_noise)

	print("x signal counts 1: ",x_basis_signal_1)
	print("x noise counts 1: ",x_basis_noise_1)

	print("X Swapping Fidelity: ",fidelity_x)
	print("X Swapping Error: ",total_error_x)

	print("X Swapping Fidelity 1: ",fidelity_x_1)
	print("X Swapping Error 1: ",total_error_x_1)

	print("BSMs: ",BSM)

	print("Alice Mu: ", alice_noise/alice_signal)
	print("Bob Mu: ", bob_noise/bob_signal)







except KeyboardInterrupt:
	print("Quit")
