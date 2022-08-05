import numpy as np
import matplotlib.pyplot as plt

input_powers = [29.9,60.4,99,138,218]
output_powers = [8.9,46,127,228,433]

plt.plot(input_powers,output_powers,marker='o',ls='--')
plt.xlabel("Input Powers (mW)")
plt.ylabel(r"Output Powers ($\mu W$)")
plt.grid(which='major',alpha=0.5)

plt.show()
