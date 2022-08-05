import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

no_combiner = np.loadtxt("TagsHistogram_no_combiner_test.txt", delimiter=';')
one_combiner = np.loadtxt("TagsHistogram_one_combiner_test.txt", delimiter=';')
two_combiner = np.loadtxt("TagsHistogram_two_combiner_test.txt", delimiter=';')

no_combiner_counts = np.array([n[1] for n in no_combiner])
one_combiner_counts = np.array([n[1] for n in one_combiner])
two_combiner_counts = np.array([n[1] for n in two_combiner])

def Gauss(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

no_max = np.argmax(no_combiner_counts)
one_max = np.argmax(one_combiner_counts)
two_max = np.argmax(two_combiner_counts)

no_combiner_counts = no_combiner_counts[no_max-30:no_max+30]
one_combiner_counts = one_combiner_counts[one_max-30:one_max+30]
two_combiner_counts = two_combiner_counts[two_max-30:two_max+30]

p0= [1/20,300,80]

no_parameters, no_covariance = curve_fit(Gauss, [i*10 for i in range(len(no_combiner_counts))], no_combiner_counts,p0=p0)
one_parameters, one_covariance = curve_fit(Gauss, [i*10 for i in range(len(one_combiner_counts))], one_combiner_counts,p0=p0)
two_parameters, two_covariance = curve_fit(Gauss, [i*10 for i in range(len(two_combiner_counts))], two_combiner_counts, p0=p0)

print(no_parameters)
print(one_parameters)
print(two_parameters)

x_all = [i*10 for i in range(len(no_combiner_counts))]

plt.plot(x_all,no_combiner_counts,ls='',marker='o',color='blue',label='no combiner')
plt.plot(x_all,[Gauss(x,no_parameters[0],no_parameters[1],no_parameters[2]) for x in x_all],color='blue',label='no combiner fit, sigma={}'.format(no_parameters[2]))
plt.plot(x_all,one_combiner_counts,ls='',marker='o',color='orange',label='one combiner')
plt.plot(x_all,[Gauss(x,one_parameters[0],one_parameters[1],one_parameters[2]) for x in x_all],color='orange',label='one combiner fit, sigma={}'.format(one_parameters[2]))
plt.plot(x_all,two_combiner_counts,ls='',marker='o',color='green',label='two combiner')
plt.plot(x_all,[Gauss(x,two_parameters[0],two_parameters[1],two_parameters[2]) for x in x_all],color='green',label='two combiner fit, sigma={}'.format(two_parameters[2]))

plt.legend()

plt.xlabel(r"$\Delta T$ (ps)")
plt.ylabel("Counts/s")

plt.show()
