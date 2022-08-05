import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def load_data(bandwidth):
    return np.loadtxt("TagsHistogram_{}pmband_120pspulse.txt".format(bandwidth), delimiter=';')

bw_32 = load_data(32)
bw_64 = load_data(64)
bw_84 = load_data(84)
bw_100 = load_data(100)
bw_150 = load_data(150)
bw_200 = load_data(200)

bw_32_counts = np.array([n[1] for n in bw_32])
bw_64_counts = np.array([n[1] for n in bw_64])
bw_84_counts = np.array([n[1] for n in bw_84])
bw_100_counts = np.array([n[1] for n in bw_100])
bw_150_counts = np.array([n[1] for n in bw_150])
bw_200_counts = np.array([n[1] for n in bw_200])

def Gauss(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

p0= [1/20,300,80]

x_all = [i*5 for i in range(len(bw_32_counts))]

def fit(points):
    return curve_fit(Gauss,x_all,points,p0=p0)

bw_32_fit = fit(bw_32_counts)
bw_64_fit = fit(bw_64_counts)
bw_84_fit = fit(bw_84_counts)
bw_100_fit = fit(bw_100_counts)
bw_150_fit = fit(bw_150_counts)
bw_200_fit = fit(bw_200_counts)

plt.plot(x_all,bw_32_counts,ls='',marker='o',color='blue',label='32pm bandwidth')
plt.plot(x_all,[Gauss(x,bw_32_fit[0][0],bw_32_fit[0][1],bw_32_fit[0][2]) for x in x_all],color='blue',label='32pm bandwidth, sigma={}'.format(bw_32_fit[0][2]))
plt.plot(x_all,bw_64_counts,ls='',marker='o',color='orange',label='64pm bandwidth')
plt.plot(x_all,[Gauss(x,bw_64_fit[0][0],bw_64_fit[0][1],bw_64_fit[0][2]) for x in x_all],color='orange',label='64pm bandwidth, sigma={}'.format(bw_64_fit[0][2]))
plt.plot(x_all,bw_84_counts,ls='',marker='o',color='green',label='84pm bandwidth')
plt.plot(x_all,[Gauss(x,bw_84_fit[0][0],bw_84_fit[0][1],bw_84_fit[0][2]) for x in x_all],color='green',label='84pm bandwidth, sigma={}'.format(bw_84_fit[0][2]))
plt.plot(x_all,bw_100_counts,ls='',marker='o',color='red',label='100pm bandwidth')
plt.plot(x_all,[Gauss(x,bw_100_fit[0][0],bw_100_fit[0][1],bw_100_fit[0][2]) for x in x_all],color='red',label='100pm bandwidth, sigma={}'.format(bw_100_fit[0][2]))
plt.plot(x_all,bw_150_counts,ls='',marker='o',color='magenta',label='64pm bandwidth')
plt.plot(x_all,[Gauss(x,bw_150_fit[0][0],bw_150_fit[0][1],bw_150_fit[0][2]) for x in x_all],color='magenta',label='150pm bandwidth, sigma={}'.format(bw_150_fit[0][2]))
plt.plot(x_all,bw_200_counts,ls='',marker='o',color='cyan',label='200pm bandwidth')
plt.plot(x_all,[Gauss(x,bw_200_fit[0][0],bw_200_fit[0][1],bw_200_fit[0][2]) for x in x_all],color='cyan',label='200pm bandwidth, sigma={}'.format(bw_200_fit[0][2]))

plt.xlim(350,1050)

plt.legend()

plt.xlabel(r"$\Delta T$ (ps)")
plt.ylabel("Counts/s")

plt.show()

contents = ['norm','x0','sigma']

print("Bandwidth: ",contents)
print("32 pm: ", bw_32_fit[0])
print("64 pm: ", bw_64_fit[0])
print("84 pm: ", bw_84_fit[0])
print("100 pm: ", bw_100_fit[0])
print("150 pm: ", bw_150_fit[0])
print("200 pm: ", bw_200_fit[0])
