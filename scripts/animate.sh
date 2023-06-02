#!/bin/bash

#SBATCH -n 4
#SBATCH --time=01:30:00
#SBATCH --mem-per-cpu=2048
#SBATCH --job-name=anim
#SBATCH --output=slurm/anim_output.txt
#SBATCH --error=slurm/anim_error.txt
#SBATCH --open-mode=truncate
#SBATCH --constraint=EPYC_7742

module restore
module load gcc/6.3.0 python ffmpeg
# module load gcc/4.8.5 python ffmpeg
module list

lscpu

cd ../tools/

time python animate.py blast_part_2 100 temperature

cd ../run/