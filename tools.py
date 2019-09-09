#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# secondary functions
#

"""
Created on Wed Nov  1 23:34:29 2017

@author: rodrigo
"""

from scipy import signal
import numpy as np
import time
import pandas as pd
from brian2 import *
from itertools import chain
###############################################################################
# Spectrum -- units are f in [Hz], Pxx in [1/s]
###############################################################################

def Sxx(x,dt=0.1,time=2):
    f, Pxx = signal.welch(x, fs=1/dt, nperseg=len(x))
    Pxx = 1000*Pxx/time
    f = f*1000
    return f, Pxx

###############################################################################
# Build hierarchical and modular network
###############################################################################

def net(p=0.0001,m=4,n_pop_pre=10000,R=0.9,seed=0):
    np.random.seed(seed)
    start = time.time()

    ratio_in_ex = 0.2
    Rex = R
    n_pop_post=n_pop_pre
    R = Rex

    listsyn_pre = []
    listsyn_post = []
    list_type =[]

    #Criacao da rede aleatoria com conexoes pre-definidas
    listsyn_pre = np.random.randint(0,high=n_pop_post,size=int(n_pop_post*n_pop_post*p))
    listsyn_post = np.random.randint(0,high=n_pop_post,size=int(n_pop_post*n_pop_post*p))

    listsyn_pre=np.asarray(listsyn_pre)
    listsyn_post=np.asarray(listsyn_post)
    
    for i in range(0,n_pop_pre):
        sort = np.random.uniform(low=0,high=1)
        if (sort>ratio_in_ex):
            list_type.append(1)
        else:
            list_type.append(-1)

    nmod = 1
    print("building network...\n")
    for i in range(1,m+1):
        print(n_pop_post)
        n_pop_post = n_pop_post/2
        nmod = nmod*2
        idd = 0
        while (idd < len(listsyn_pre)):
            n1 = 1; n2 = 1;
            mod1 = 0; mod2 = 0
            while (listsyn_post[idd] > (mod2 + n_pop_post)):
                mod2 = mod2+n_pop_post
                n2 = n2+1
            while (listsyn_pre[idd] > (mod1 + n_pop_post)):
                mod1 = mod1+n_pop_post
                n1 = n1+1
                
            if (n1!=n2 and list_type[listsyn_pre[idd]]<0):
                nn = mod1 + (int((np.random.uniform(low=0,high=1))*n_pop_post))
                listsyn_post[idd] = nn
            
            if (n1!=n2 and list_type[listsyn_pre[idd]]>0):
                sort = np.random.uniform(low=0,high=1)
                if (sort < Rex):
                    nn = mod1+(int((np.random.uniform(low=0,high=1))*n_pop_post))
                    listsyn_post[idd] = nn
            idd = idd+1

    listsyn_pre_ex = []
    listsyn_post_ex = []
    listsyn_pre_in = []
    listsyn_post_in = []
    idd=0
    while (idd < len(listsyn_pre)):
        if (list_type[listsyn_pre[idd]]>0):
            listsyn_pre_ex.append(listsyn_pre[idd])
            listsyn_post_ex.append(listsyn_post[idd])
        else:
            listsyn_pre_in.append(listsyn_pre[idd])
            listsyn_post_in.append(listsyn_post[idd])
        idd = idd+1

    listsyn_pre_ex=np.asarray(listsyn_pre_ex)
    listsyn_post_ex=np.asarray(listsyn_post_ex)
    listsyn_pre_in=np.asarray(listsyn_pre_in)
    listsyn_post_in=np.asarray(listsyn_post_in)

    end = time.time()

    elapsed = end - start
    print("time elapsed to build network ")
    print(elapsed)


    return listsyn_pre_ex,listsyn_post_ex,listsyn_pre_in,listsyn_post_in

###############################################################################
#  BRUNEL fixed in degree function -- for comparison
###############################################################################

def fixed_indegree(indegree,n_post_pop,n_pre_pop):
    
    presyn_indices = np.zeros([n_post_pop*indegree])
    postsyn_indices = np.zeros([n_post_pop*indegree])
    counter = 0
    
    for post in range(n_post_pop):
        x = np.arange(0, n_pre_pop)
        y = np.random.permutation(x)
        for i in range(indegree):
            presyn_indices[counter] = y[i]
            postsyn_indices[counter] = post
            counter += 1
    presyn_indices = presyn_indices.astype(int)
    postsyn_indices = postsyn_indices.astype(int)
    return presyn_indices, postsyn_indices

def load_raster(J, m, seed):
	file_name = 'data/spkTrains_J_'+str(J)+'_m_'+str(m)+'_seed_'+str(seed)+'.npy'
	return np.load(file_name, allow_pickle=True).item()

def convert_to_df(J, m, seed):

	file_name = 'data/spkTrains_J_'+str(J)+'_m_'+str(m)+'_seed_'+str(seed)+'.npy'

	times  = np.load(file_name, allow_pickle=True).item()
	i, t   = [], []
	for key, value in times.items():
		t.append(list(value/ms))
		i.append(np.ones(len(list(value/ms)))*key)
	t = list(chain.from_iterable(t))
	i = list(chain.from_iterable(i))
	data = np.array([i, t]).T
	data   = pd.DataFrame(data, columns=['i', 't'])
	return data

