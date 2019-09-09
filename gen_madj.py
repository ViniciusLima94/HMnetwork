from brian2 import *
import numpy as np
from tools import *
from set_params import *

idx = int(sys.argv[-1])

k=10
j=10

p1 = np.linspace(0, 9, j, dtype=int)
p2 = np.arange(1, 10000, 1000, dtype=int)

grid=np.meshgrid(p1, p2)
pars=np.reshape(grid, (2,k*j)).T 

listsyn_pre_ex,listsyn_post_ex,listsyn_pre_in,listsyn_post_in=net(p=0.01,m=pars[idx,0],n_pop_pre=N,R=0.9,seed=pars[idx,1])

np.save('conn/madj_m_'+str(pars[idx,0])+'_seed_'+str(pars[idx,1])+'.npy', {'pre_ex': listsyn_pre_ex, 'post_ex': listsyn_post_ex, 'pre_in': listsyn_pre_in, 'post_in': listsyn_post_in})