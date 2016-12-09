#!/bin/bash
# Set your minimum acceptable walltime, format: day-hours:minutes:seconds
#SBATCH --time=0-03:00:00

# Set name of job shown in squeue
# SBATCH --job-name trains_svm --output=train_svm.txt

# Request CPU resources
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1

# Memory usage (MB)
# SBATCH --mem-per-cpu=3000

# Use modules to set the software environment
module load python

python training_svm.py