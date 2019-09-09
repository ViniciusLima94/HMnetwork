# HM Network
Code to generate the topology and simulate the network used on our paper "Optimal interplay between synaptic strengths andnetwork structure enhances activity fluctuations andinformation propagation in hierarchical modularnetworks".

## Be aware when lauching the codes all of them use a lot of memory.

# Network Topology

> The code to generate the adjacency matrix is called "gen_madj.py", to run it you have to launch the script "run_madj.sh" (sbatch run_madj.sh), the adjancey matrices will be saved in the directory "conn" with name: "madj_m_X_seed_Y.npy", where X is the hierachy of the network and Y the seed used.

# Run the network  

> After running the code to generate the adjacency matrices you can run the network simulations, in the script "set_params.py" we define network parameters, the implementation of the network (in Brian 2) is in the scrip "main.py, to run the simulation lauch the script "run.sh" (sbatch run.sh), the raster plots will be saved in the directory "data" with name: "spkTrains_J_Z_m_X_seed_Y.npy", where X is the hierachy of the network, Y the seed used, and Z the value for the synaptic coupling.
