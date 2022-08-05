
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

file_names = ["WaveData20220601_000.csv", "WaveData20220601_001.csv", "WaveData20220601_002.csv", "WaveData20220601_003.csv"]
titles = ["Bob 2", "Bob 1", "Alice 1", "Alice 2"]

fig, axs = plt.subplots(4, 1, sharex = True)
for i in range(len(file_names)):
    ax = axs[i]
    df=pd.read_csv(file_names[i], skiprows = 28)
    wavelengths = df["Wavelength(A)"].to_numpy()
    y_osa = df["Level(A)"].to_numpy()
    y_osa_dBm = np.array([np.log10(y/0.001) if y>0 else np.log10(1e-10/0.001) for y in y_osa])
    ind_max = np.argmax(y_osa)
    peak_wavelength = wavelengths[ind_max]

    ax.plot(wavelengths, y_osa_dBm)
    ax.plot(peak_wavelength*np.ones(100), np.linspace(np.min(y_osa_dBm),np.max(y_osa_dBm), 100), "--k", label = "max = "+str(peak_wavelength))

    ax.set_ylabel("dBm")
    ax.legend()
    ax.set_title(titles[i])
    ax.set_xlim([1536, 1538])
    if i == 3:
        ax.set_xlabel("Wavelength (nm)")




colors = ["r", "g", "b", "m"]
fig, ax = plt.subplots(1, 1, sharex = True)
for i in range(len(file_names)):
    df=pd.read_csv(file_names[i], skiprows = 28)
    wavelengths = df["Wavelength(A)"].to_numpy()
    y_osa = df["Level(A)"].to_numpy()
    y_osa_dBm = np.array([np.log10(y/0.001) if y>0 else np.log10(1e-10/0.001) for y in y_osa])
    ind_max = np.argmax(y_osa)
    peak_wavelength = wavelengths[ind_max]
    ax.plot(wavelengths, y_osa_dBm, colors[i])
    ax.plot(peak_wavelength*np.ones(100), np.linspace(np.min(y_osa_dBm),np.max(y_osa_dBm), 100), "--"+colors[i], label = titles[i]+", max = "+str(peak_wavelength))
ax.set_ylabel("dBm")
ax.legend()
ax.set_xlabel("Wavelength (nm)")
ax.set_xlim([1536, 1538])
plt.tight_layout()
plt.show()
