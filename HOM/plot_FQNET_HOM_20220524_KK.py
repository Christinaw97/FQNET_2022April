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
delay_step_times = np.array([5,5,5,5,5,5,5,5,5,5,5,5,5,5,5])*4*60##how many seconds per step(10 minutes is 600)
adqtime_tab2=2
adqtime_histo=2


START_TIME = '2022-05-24 21:46:00'
END_TIME = '2022-05-25	00:06:30'

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


Ch0,Ch1,Ch2,Ch3 =[],[],[],[]


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
		TABLE_NAME = "TAB118_05_2022_17_33_48"
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


		TABLE_NAME = "TAB218_05_2022_17_33_48"
		queryGUI = "SELECT ch0, ch1, ch2, ch3, datetime FROM "+TABLE_NAME+" WHERE datetime BETWEEN {ts %s} AND {ts %s}"
		cur.execute(queryGUI, (START_TIME,END_TIME,))
		row = cur.fetchone()

		while row is not None:
			Ch0.append(row["ch0"])
			Ch1.append(row["ch1"])
			Ch2.append(row["ch2"])
			Ch3.append(row["ch3"])
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

	df_tab2 =pd.DataFrame(list(zip(time_tab2_el, Ch0, Ch1, Ch2, Ch3)))
	df_tab2.columns=["time_histo_el_s", "ch0", "ch1", "ch2", "ch3"]
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
	ch2_bin = []
	ch3_bin = []


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
	ch2 = 0
	ch3 = 0

	j=0

	print("I's length:", len(time_tab2_el))

	for i in range(len(time_tab2_el)):
		ch0 = ch0 + Ch0[i]
		ch1 = ch1 + Ch1[i]
		ch2 = ch2 + Ch2[i]
		ch3 = ch3 + Ch3[i]
		#print(adqtime/10)
		if j < 15 and i%round(delay_step_times[j]/adqtime_tab2)==0:
			#print(time_tab2_el[i]
			time_tab2_el_bin.append(round(time_tab2_el[i]))
			ch0_bin.append(ch0)
			ch1_bin.append(ch1)
			ch2_bin.append(ch2)
			ch3_bin.append(ch3)
			# dlh = time_histo_el[i]
			# dltab2 = time_tab2_el[i]
			#print(and2_bin)
			ch0 = Ch0[i]
			ch1 = Ch1[i]
			ch2 = Ch2[i]
			ch3 = Ch3[i]
			j=j+1





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
		if j < 15 and i%round(delay_step_times[j]/adqtime_histo)==0:
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
			j = j+1



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
	tab1_titles = ["Charlie 1", "Charlie 2", "Bob", "Alice"]#, ["Rb1", "Rb2", "Rb3"], ["Rc1","Rc2", "Rc3"]]

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

	print(time_tab2_el_bin)

	tab2_indices= range(1,len(time_tab2_el_bin)+1)

	print(tab2_indices)

	tab2_data = [ch0_bin,ch1_bin,ch2_bin,ch3_bin]
	print(tab2_data)
	tab2_titles = ["2 fold", "3 fold Heralding Bob", "3 fold Heralding Alice", "4 fold"]

	fig2, axs2 = plt.subplots(4,1, num=300, sharex = True)

	for i in range(4):
		print(tab2_indices[0],tab2_indices[-1])
		print(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]])
		print(tab2_data[i][tab2_indices[0]:tab2_indices[-1]])
		axs2[i].plot(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]],
		tab2_data[i][tab2_indices[0]:tab2_indices[-1]],
		 linestyle = 'none', marker = '.', markersize = 8)
		axs2[i].set_ylabel(tab2_titles[i])
	axs2[3].set_xlabel('Elapsed time (s)', fontsize =16)

	plt.show()

	fig3, axs3 = plt.subplots(4,1, num=500, sharex = True)

	meanCounts=np.mean(d0_bin)
	normD0Array= np.array(d0_bin)/meanCounts

	for i in range(4):
		print(tab2_indices[0],tab2_indices[-1])
		print(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]])
		print(tab2_data[i][tab2_indices[0]:tab2_indices[-1]])
		axs3[i].plot(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]],
		tab2_data[i][tab2_indices[0]:tab2_indices[-1]]/normD0Array[tab2_indices[0]:tab2_indices[-1]],
		 linestyle = 'none', marker = '.', markersize = 8)
		axs3[i].set_ylabel(tab2_titles[i])
	axs3[3].set_xlabel('Elapsed time (s)', fontsize =16)

	fig4, axs4 = plt.subplots(4,1, num=600, sharex = True)

	meanCounts_c=np.mean(c0_bin)
	normC0Array= np.array(c0_bin)/meanCounts_c

	for i in range(4):
		print(tab2_indices[0],tab2_indices[-1])
		print(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]])
		print(tab2_data[i][tab2_indices[0]:tab2_indices[-1]])
		axs4[i].plot(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]],
		tab2_data[i][tab2_indices[0]:tab2_indices[-1]]/normC0Array[tab2_indices[0]:tab2_indices[-1]],
		 linestyle = 'none', marker = '.', markersize = 8)
		axs4[i].set_ylabel(tab2_titles[i])
	axs4[3].set_xlabel('Elapsed time (s)', fontsize =16)

	fig5, axs5 = plt.subplots(4,1, num=700, sharex = True)

	#meanCounts_b=np.mean(b0_bin)
	#normB0Array= np.array(b0_bin)/meanCounts_b

	for i in range(4):
		print(tab2_indices[0],tab2_indices[-1])
		print(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]])
		print(tab2_data[i][tab2_indices[0]:tab2_indices[-1]])
		axs5[i].plot(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]],
		tab2_data[i][tab2_indices[0]:tab2_indices[-1]]/normC0Array[tab2_indices[0]:tab2_indices[-1]]/normD0Array[tab2_indices[0]:tab2_indices[-1]],
		 linestyle = 'none', marker = '.', markersize = 8)
		axs5[i].set_ylabel(tab2_titles[i])
	axs5[3].set_xlabel('Elapsed time (s)', fontsize =16)

	plt.show()

	fig5, axs5 = plt.subplots(4,1, num=800, sharex = True)

	meanCounts_b=np.mean(b0_bin)
	normB0Array= np.array(b0_bin)/meanCounts_b
	meanCounts_a=np.mean(a0_bin)
	normA0Array= np.array(a0_bin)/meanCounts_a

	for i in range(4):
		print(tab2_indices[0],tab2_indices[-1])
		print(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]])
		print(tab2_data[i][tab2_indices[0]:tab2_indices[-1]])
		axs5[i].plot(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]],
		tab2_data[i][tab2_indices[0]:tab2_indices[-1]]/normC0Array[tab2_indices[0]:tab2_indices[-1]]/normA0Array[tab2_indices[0]:tab2_indices[-1]]/normB0Array[tab2_indices[0]:tab2_indices[-1]],
		 linestyle = 'none', marker = '.', markersize = 8)
		axs5[i].set_ylabel(tab2_titles[i])
	axs5[3].set_xlabel('Elapsed time (s)', fontsize =16)

	plt.show()

	times = [-2140]

	time = -2140 + 8*240
	times.append(time)
	for i in range(4):
		time = time + 240
		times.append(time)

	steps = [6,10,2,2,1,1,1,1,1,1,2,2,10,6]

	hom_counts_no_norm = tab2_data[2][tab2_indices[0]:tab2_indices[-1]]
	hom_counts_norm_both = tab2_data[0][tab2_indices[0]:tab2_indices[-1]]/normD0Array[tab2_indices[0]:tab2_indices[-1]]/normC0Array[tab2_indices[0]:tab2_indices[-1]]

	hom_counts_norm_a = tab2_data[2][tab2_indices[0]:tab2_indices[-1]]/normD0Array[tab2_indices[0]:tab2_indices[-1]]
	hom_counts_norm_b = tab2_data[3][tab2_indices[0]:tab2_indices[-1]]/normC0Array[tab2_indices[0]:tab2_indices[-1]]


	print(hom_counts_no_norm)

	HOM_data = [[sum(steps[:i])*40,h] for i, h in enumerate(hom_counts_norm_b)]
	HOM_df = pd.DataFrame(HOM_data,columns=['delay_(ps)','counts_per_90_min'])
	#HOM_df.to_csv('HOM_20220523_4f_norm_b.csv',index=False)






except KeyboardInterrupt:
	print("Quit")
