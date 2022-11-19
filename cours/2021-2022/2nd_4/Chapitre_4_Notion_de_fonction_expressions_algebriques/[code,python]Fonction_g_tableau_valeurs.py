from lycee import *
def g(x):
    return x**3-2*x**2-4*x-5

for i in range(-2,7):
    print(g(i/2))

import numpy as np
for i in np.arange (-1,3.5,0.5):
    print(g(i))