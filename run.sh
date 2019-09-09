#!/bin/bash

#SBATCH -J HMN                    # Job name
#SBATCH -o ./out/HMN_%a.out             # Name of stdout output file (%j expands to %jobID)
#SBATCH -t 700:00:00              # Run time (hh:mm:ss) - 1.5 hours
#SBATCH -N 1 
#SBATCH --exclude=c[01-04],clusterneuromat
#SBATCH --array=0-999

module load py36-brian2/2.2.2.1
python3 main.py $SLURM_ARRAY_TASK_ID
