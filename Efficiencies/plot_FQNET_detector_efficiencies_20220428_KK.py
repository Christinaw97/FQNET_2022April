import numpy as np
import matplotlib.pyplot as plt

bias_voltages = [.045+0.005*i for i in range(11)]

B1_eff_rates = np.array([2,2,6,3.7e3,240e3,1.45e6,2.89e6,4.1e6,4.7e6,5.2e6,5.4e6])
B1_dark_rates = np.array([2,2,8,62,70,80,108,150,190,370,1750])

B2_eff_rates = np.array([20,4.9e3,270e3,1.6e6,3.1e6,3.9e6,4.2e6,4.3e6,4.5e6,4.6e6,4.6e6])
B2_dark_rates = np.array([20,40,40,66,76,104,132,270,1200,6000,16000])

B3_eff_rates = np.array([22,2e3,175e3,1.57e6,3.6e6,5e6,5.7e6,6.1e6,6.5e6,6.6e6,7e6])
B3_dark_rates = np.array([30,72,74,82,126,140,156,280,880,4700,2000000])

B4_eff_rates = np.array([16,174,25e3,500e3,2.17e6,4e6,5.2e6,5.8e6,6.15e6,6.5e6,6.65e6])
B4_dark_rates = np.array([44,58,68,76,84,118,130,132,202,516,2500])

B1_max_rate = 8.54e6
B2_max_rate = 8.31e6
B3_max_rate = 8.78e6
B4_max_rate = 7.79e6

B1_eff = B1_eff_rates/B1_max_rate
B2_eff = B2_eff_rates/B2_max_rate
B3_eff = B3_eff_rates/B3_max_rate
B4_eff = B4_eff_rates/B4_max_rate

fig1,axs1 = plt.subplots(2,1,num=100,sharex=True)

axs1[0].plot(bias_voltages,B1_eff,marker='o',ls='--')
axs1[1].plot(bias_voltages,B1_dark_rates,marker='o',ls='--',color='red')
axs1[1].set_yscale('log')
axs1[0].grid(which='major',alpha=0.5)
axs1[1].grid(which='major',alpha=0.5)
axs1[1].grid(which='minor',alpha=0.2)
axs1[0].set_ylabel('B1 Efficiencies')
axs1[1].set_ylabel('Dark Count Rate (Hz)')
axs1[1].set_xlabel("Bias Voltage")

plt.show()

fig2,axs2 = plt.subplots(2,1,num=200,sharex=True)

axs2[0].plot(bias_voltages,B2_eff,marker='o',ls='--')
axs2[1].plot(bias_voltages,B2_dark_rates,marker='o',ls='--',color='red')
axs2[1].set_yscale('log')
axs2[0].grid(which='major',alpha=0.5)
axs2[1].grid(which='major',alpha=0.5)
axs2[1].grid(which='minor',alpha=0.2)
axs2[0].set_ylabel('B2 Efficiencies')
axs2[1].set_ylabel('Dark Count Rate (Hz)')
axs2[1].set_xlabel("Bias Voltage")

plt.show()

fig3,axs3 = plt.subplots(2,1,num=300,sharex=True)

axs3[0].plot(bias_voltages,B3_eff,marker='o',ls='--')
axs3[1].plot(bias_voltages,B3_dark_rates,marker='o',ls='--',color='red')
axs3[1].set_yscale('log')
axs3[0].grid(which='major',alpha=0.5)
axs3[1].grid(which='major',alpha=0.5)
axs3[1].grid(which='minor',alpha=0.2)
axs3[0].set_ylabel('B3 Efficiencies')
axs3[1].set_ylabel('Dark Count Rate (Hz)')
axs3[1].set_xlabel("Bias Voltage")

plt.show()

fig4,axs4 = plt.subplots(2,1,num=400,sharex=True)

axs4[0].plot(bias_voltages,B4_eff,marker='o',ls='--')
axs4[1].plot(bias_voltages,B4_dark_rates,marker='o',ls='--',color='red')
axs4[1].set_yscale('log')
axs4[0].grid(which='major',alpha=0.5)
axs4[1].grid(which='major',alpha=0.5)
axs4[1].grid(which='minor',alpha=0.2)
axs4[0].set_ylabel('B1 Efficiencies')
axs4[1].set_ylabel('Dark Count Rate (Hz)')
axs4[1].set_xlabel("Bias Voltage")

plt.show()
