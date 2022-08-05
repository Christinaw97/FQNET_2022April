import numpy as np
import matplotlib.pyplot as plt

def two_fold(u_a,u_b,n_a2,n_b1,z):
    numerator = 8*(1+n_a2*u_a)*(1+n_b1*u_b)*(-np.abs(-2*(2+n_b1*u_b)+
                n_a2*u_a*(-2+(-1+z**2)*n_b1*u_b))+(2+n_a2*u_a)*(2+n_b1*u_b))
    denominator = np.abs(-2*(2+n_b1*u_b)+n_a2*u_a*(-2+(-1+z**2)*n_b1*u_b))*(2*n_b1**2*u_b**2+n_a2*n_b1*u_a*u_b*(2+3*n_b1*u_b)+n_a2**2*u_a**2*(2+3*n_b1*u_b+n_b1**2*u_b**2))

    return numerator/denominator

z_points = np.arange(0,1,0.01)

print(z_points)

u_a = 1.64e-2
u_b = 3.61e-2
n_a2 = 0.005
n_b1 = 0.01

plt.plot(z_points,[two_fold(u_a,u_b,n_a2,n_b1,z) for z in z_points])
plt.xlabel(r'$\zeta$')
plt.ylabel('visibility')
plt.title('FQNET',loc='left')
plt.show()
