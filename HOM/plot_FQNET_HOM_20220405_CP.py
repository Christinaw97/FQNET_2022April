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
delay_step_time = 1200##how many seconds per step(10 minutes is 600)
adqtime_tab2=1
adqtime_histo=1


START_TIME = '2022-04-05 20:17:00'
END_TIME = '2022-04-06 00:57:00'

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



	cur_file_base = os.path.basename(__file__)
	cur_file_name = os.path.splitext(cur_file_base)[0]
	csv_filename_histo= cur_file_name+"_histo.csv"
	csv_filename_tab2= cur_file_name+"_tab2.csv"
	path_to_file ="/home/fqnet/Software/FQNET/FQNET_HOM_2022April/"
	df_histo =pd.DataFrame(list(zip(time_histo_el, Ra1, Ra2, Ra3, Rb1, Rb2, Rb3, Rc1, Rc2, Rc3)))
	df_histo.columns=["time_histo_el_s", "Ra1", "Ra2", "Ra3", "Rb1", "Rb2","Rb3", "Rc1", "Rc2", "Rc3"]
	df_histo.to_csv(path_to_file+csv_filename_histo)

	df_tab2 =pd.DataFrame(list(zip(time_tab2_el, and1, and2, and3, or_gate,bsm1, bsm2)))
	df_tab2.columns=["time_histo_el_s", "and1", "and2", "and3", "or", "bsm1","bsm2"]
	df_tab2.to_csv(path_to_file+csv_filename_tab2)



   #print(time_histo_el)
       #print(time_tab2_el)

    #histo_indices = np.where(time_histo_el > time_tab2_el[0])
   #histo_indices = histo_indices[0]

       #time_histo_el = time_histo_el[histo_indices[0]:histo_indices[-1]]

  #Ra1 = Ra1[histo_indices[0]:histo_indices[-1]]
 #Rb1 = Rb1[histo_indices[0]:histo_indices[-1]]
        #Rc1 = Rc1[histo_indices[0]:histo_indices[-1]]


	time_histo_el_bin = []
	time_tab2_el_bin = []
	and1_bin = []
	and2_bin = []
	and3_bin = []
	or_bin = []
	bsm1_bin = []
	Ra1_bin = []
	Rb1_bin = []
	Rc1_bin = []


	a1 = 0
	a2 = 0
	a3 = 0
	o = 0
	bs = 0
	for i in range(len(time_tab2_el)):
             a1 = a1 + and1[i]
             a2 = a2 + and2[i]
             a3 = a3 + and3[i]
             o = o + or_gate[i]
             bs = bs + bsm1[i]

              #print(adqtime/10)
             if i%round(delay_step_time/adqtime_tab2)==0:
                      #print(time_tab2_el[i]
                 time_tab2_el_bin.append(round(time_tab2_el[i]))
                 and1_bin.append(a1)
                 and2_bin.append(a2)
                 and3_bin.append(a3)
                 or_bin.append(o)
                 bsm1_bin.append(bs)
                 # dlh = time_histo_el[i]
                 # dltab2 = time_tab2_el[i]
                 print(and2_bin)
                 a1 = and1[i]
                 a2 = and2[i]
                 a3 = and3[i]
                 o = or_gate[i]
                 bs = bsm1[i]




	ra = 0
	rb = 0
	rc = 0
	print("After binning for loop")
	print(bsm1_bin)
	for i in range(len(time_histo_el)):
		ra = ra + Ra1[i]
		rb = rb + Rb1[i]
		rc = rc + Rc1[i]
		if i%round(delay_step_time/adqtime_histo)==0:
			#print(time_histo_el[i])
			time_histo_el_bin.append(round(time_histo_el[i]))
			Ra1_bin.append(ra)
			Rb1_bin.append(rb)
			Rc1_bin.append(rc)
			ra = Ra1[i]
			rb = Rb1[i]
			rc = Rc1[i]


















	time_histo_el_mins=np.array(time_histo_el_mins)
	time_tab2_el_mins=np.array(time_tab2_el_mins)
	time_histo_el_bin = np.array(time_histo_el_bin)
	time_tab2_el_bin = np.array(time_tab2_el_bin)
	and1_bin = np.array(and1_bin)
	and2_bin = np.array(and2_bin)
	and3_bin = np.array(and3_bin)
	or_bin = np.array(or_bin)
	bsm1_bin = np.array(bsm1_bin)
	Ra1_bin = np.array(Ra1_bin)
	Rb1_bin = np.array(Rb1_bin)
	Rc1_bin = np.array(Rc1_bin)

	print("After making binning numpy array")
	print(bsm1_bin)



	#Stacked plot of all data

	fig1, axs = plt.subplots(3,1, num=238, sharex = True)
	# xmin=time_Vap_el_mins[0] #40
	# xmax=time_Vap_el_mins[-1] #60

	#histo_indices = np.where(time_histo_el_mins > time_Vap_el_mins[0])
	#histo_indices = histo_indices[0]


	histo_indices= range(1,len(time_histo_el_bin))

	tab1_data = [Ra1_bin, Rb1_bin, Rc1_bin]#, [Rb1, Rb2, Rb3], [Rc1, Rc2, Rc3]]
	tab1_titles = ["Ra1", "Rb1", "Rc1"]#, ["Rb1", "Rb2", "Rb3"], ["Rc1","Rc2", "Rc3"]]

	print(len(histo_indices), 'len histo indicies')

	# NEW_time_histo_el_mins=[]
	# print(time_histo_el_mins, 'histo')
	# for a in range(0,len(time_histo_el_mins)):
	# 	NEW_time_histo_el_mins.append(round(time_histo_el_mins[a]))
	# print(len(tab1_data[1]), 'tabl_data len')
	# #[len(a) for a in my_tuple_2d]
	meanCounts=np.mean(Rc1_bin)
	normRA1Array= np.array(Ra1_bin)/meanCounts
	normRB1Array= np.array(Rb1_bin)/meanCounts
	normRC1Array= np.array(Rc1_bin)/meanCounts
        #print(len(Ra1_bin), len(and1_bin), 'RA1 len', 'and1bin len' )
        #print(meanCounts)

	for i in range(3):
		#for j in range(1):
		axs[i].plot(time_histo_el_bin[histo_indices[0]:histo_indices[-1]], tab1_data[i][histo_indices[0]:histo_indices[-1]],  linestyle = 'none', marker= '.', markersize=8)
		axs[i].set_ylabel(tab1_titles[i])
	axs[2].set_xlabel('Elapsed time (s)', fontsize =16)



	##Saving Counts Plots into Disk
	fig1.savefig('counts.png')
	fig1.savefig('counts.pdf')



	#Plotting 2 and 3 fold
	fig2, axs2 = plt.subplots(2,1, num=500, sharex = True)


	tab2_indices= range(1,len(time_tab2_el_bin))

	tab2_data= [and2_bin, bsm1_bin]
	tab2_titles = ['Two Folds', 'Three Folds']

	for i in range(2):
		#for j in range(1):
		axs2[i].plot(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]],
		tab2_data[i][tab2_indices[0]:tab2_indices[-1]],
		 linestyle = 'none', marker = '.', markersize = 8)
		axs2[i].set_ylabel(tab2_titles[i])
		axs2[1].set_xlabel('Elapsed time (s)', fontsize =16)

	##Saving HOM plots to disk
	fig2.savefig('hom_NoNormalization.png')
	fig2.savefig('hom_NoNormalization.pdf')

	tab2_titles_normalized = ['Two Folds Normalized', 'Three Folds Normalized']
	fig3, axs3 = plt.subplots(2,1, num=600, sharex = True)
	for i in range(2):
		#for j in range(1):
		axs3[i].plot(time_tab2_el_bin[tab2_indices[0]:tab2_indices[-1]],
		tab2_data[i][tab2_indices[0]:tab2_indices[-1]]/normRC1Array[tab2_indices[0]:tab2_indices[-1]],
		 linestyle = 'none', marker = '.', markersize = 8)
		axs3[i].set_ylabel(tab2_titles_normalized[i])
		axs3[1].set_xlabel('Elapsed time (s)', fontsize =16)





	##Saving HOM Normalized Counts to Disk###
	fig3.savefig('hom_Normalized.png')
	fig3.savefig('hom_Normalized.pdf')

	tab4_data = [Ra1,Rb1,Rc1]
	tab4_titles = ['Ra1','Rb1','Rc1']

	fig4, axs4 = plt.subplots(3,1, num=700, sharex = True)

	for i in range(3):
		#for j in range(1):
		axs4[i].plot(time_histo_el, tab4_data[i],  linestyle = '-')
		axs4[i].set_ylabel(tab4_titles[i])
	axs4[2].set_xlabel('Elapsed time (s)', fontsize =16)

	##Saving Counts Plots into Disk
	fig4.savefig('counts_tot.png')
	fig4.savefig('counts_tot.pdf')

	tab5_data = [and2,bsm1]
	tab5_titles = ['and2','bsm1']
	fig5,ax5 = plt.subplots(2,1, num=800, sharex = True)

	for i in range(2):
		ax5[i].plot(time_histo_el,tab5_data[i],linestyle='-')
		ax5[i].set_ylabel(tab5_titles[i])
	ax5[1].set_xlabel('Elapsed time (s)', fontsize =16)


	delta_t = [-730+120*i for i in range(12)]
	hom_counts = tab2_data[0][tab2_indices[0]:tab2_indices[-1]]/normRC1Array[tab2_indices[0]:tab2_indices[-1]]
	hom_counts_three = tab2_data[1][tab2_indices[0]:tab2_indices[-1]]/normRC1Array[tab2_indices[0]:tab2_indices[-1]]

	hom_counts_no_norm = tab2_data[0][tab2_indices[0]:tab2_indices[-1]]

	hom_counts_no_norm_three = tab2_data[1][tab2_indices[0]:tab2_indices[-1]]

	HOM_data = np.array([[d_t,hom_counts[i]] for i, d_t in enumerate(delta_t)])

	HOM_data_three = np.array([[delta_t[i],hom_counts_three[i]] for i in range(2,12)])

	HOM_data_no_norm = np.array([[d_t,hom_counts_no_norm[i]] for i, d_t in enumerate(delta_t)])

	HOM_data_no_norm_three = np.array([[d_t,hom_counts_no_norm_three[i]] for i, d_t in enumerate(delta_t)])

	print(HOM_data_three)

	print(HOM_data.shape)
	HOM_df = pd.DataFrame(HOM_data,columns=['delay_(ps)','counts_per_20_min'])
	HOM_df.to_csv('HOM_20220405.csv',index=False)

	HOM_df_3 = pd.DataFrame(HOM_data_three,columns=['delay_(ps)','counts_per_20_min'])
	HOM_df_3.to_csv('HOM_20220405_3f.csv',index=False)

	#plt.show()
	print("")

	print("time_tab2_last=",time_tab2_last )
	print("time_histo_last=",time_histo_last )
	plt.show()


except KeyboardInterrupt:
	print("Quit")
