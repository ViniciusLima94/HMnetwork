#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  1 23:34:29 2017

@author: rodrigo
"""
from brian2 import *
import numpy as np
from tools import *
import matplotlib.pyplot as plt
import sys
from set_params import *
#import os

#try:
#    os.system('rm -R __pycache__')
#except:
#    None

#clear_cache('cython')

###############################################################################
# Parallel setup
###############################################################################

idx = int(sys.argv[-1])

m = int(pars[idx,1])
J = pars[idx,0]*mV
seed = int(pars[idx,2])
###############################################################################
# Parameters
###############################################################################

modules_number = 2**m
modules_size = N/modules_number
np.random.seed(seed)

record = True
plot = False

###############################################################################
# Network
###############################################################################

eqs = '''
dv/dt = (-v + RI)/tau	: volt (unless refractory)
RI : volt
'''
Neurons = NeuronGroup(N,eqs,threshold='v>=20*mV',reset='v=vr',refractory=0.5*ms, method='euler',dt=dt)
Neurons.RI = 30*mV
Neurons.v='rand()*(20-10)*mV + vr'
#Neurons[9000:].RI = 70*mV

#listsyn_pre_ex,listsyn_post_ex,listsyn_pre_in,listsyn_post_in=net(p=0.01,m=m,n_pop_pre=N,R=0.9,seed=seed)
listsyn_pre_ex  = np.load('conn/madj_m_'+str(m)+'_seed_'+str(seed)+'.npy').item()['pre_ex']
listsyn_post_ex = np.load('conn/madj_m_'+str(m)+'_seed_'+str(seed)+'.npy').item()['post_ex']
listsyn_pre_in  = np.load('conn/madj_m_'+str(m)+'_seed_'+str(seed)+'.npy').item()['pre_in']
listsyn_post_in = np.load('conn/madj_m_'+str(m)+'_seed_'+str(seed)+'.npy').item()['post_in']

Sinapse_ex = Synapses(Neurons, Neurons, on_pre='v+=J',delay=D,dt=0.1*ms)
Sinapse_ex.connect(i=listsyn_pre_ex,j=listsyn_post_ex)

Sinapse_in = Synapses(Neurons, Neurons, on_pre='v-=J*g',delay=D,dt=0.1*ms)
Sinapse_in.connect(i=listsyn_pre_in,j=listsyn_post_in)

SpikeMon = SpikeMonitor(Neurons)
Ratemon = PopulationRateMonitor(Neurons)

run(sim,report ='stdout')

###############################################################################
# Power spectrum statistics
###############################################################################

spks = SpikeMon.spike_trains()
# Sbar=np.zeros( (modules_number, int((sim/ms)/(dt/ms))/2 + 1 ) )

# for j in range(0,modules_number):
#     for i in range(j*modules_size,j*modules_size + trials_statistics):
#         x = np.zeros(int((sim/ms)/(dt/ms)))
#         a=(spks[i]/ms)/(dt/ms)
#         x[a.astype(int)]=1/(dt/ms)
#         f,S = Sxx(x)
#         Sbar[j,:] = Sbar[j,:] + S

# Sbar = Sbar/trials_statistics

#if (record):
filename='data/spkTrains_J_'+str(np.round(J/mV,1))+'_m_' + str(m) + '_seed_'+str(seed)+'.npy'
np.save(filename,spks)
    # np.savetxt('Sxx_seed_'+str(seed)+'_m_' + str(m) + '.dat',np.transpose(Sbar),delimiter='\t')

###############################################################################
# Plots
###############################################################################

if(0):
    plt.figure(figsize=(10,8))
    plt.subplot(211)
    plt.plot(SpikeMon.t,SpikeMon.i,'.',ms=0.1)
    plt.subplot(212)
    plt.plot(Ratemon.t/ms,Ratemon.rate/Hz)
    plt.show()

if(plot):
    for i in range(0,modules_number):
        plt.loglog(f,Sbar[i,:],label='module ' + str(i))
    plt.legend()
    plt.xlabel('frequency [Hz]')
    plt.ylabel('[1/s]')
    plt.xlim((1,1000))
    plt.ylim((1,1000))
    plt.show()
