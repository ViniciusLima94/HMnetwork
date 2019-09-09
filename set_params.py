import numpy as np 
from brian2 import *

###############################################################################
# Grid of parameters to swap
###############################################################################

k=10
j=10
p1 = np.linspace(0.1, 1, k) # Array size k : J
p2 = np.linspace(0, 9, j) # Array size j : m
p3 = np.arange(1, 10000, 1000, dtype=int)

grid=np.meshgrid(p1, p2,p3) # Meshigrid
pars=np.reshape(grid, (3,k*j*len(p3))).T # Every pair possible formed by p1 and p2

###############################################################################
# Networks parameters 
###############################################################################

dt=0.1*ms
defaultclock.dt = dt
N=131072

g=5
D=0.55*ms
vr=10*mV
tau=20*ms

sim = 2000*ms
trials_statistics=100
