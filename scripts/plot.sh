#!/bin/bash

#SBATCH -n 1
#SBATCH --time=02:00:00
#SBATCH --mem-per-cpu=8192
#SBATCH --job-name=plot
#SBATCH --output=slurm/plot_output.txt
#SBATCH --error=slurm/plot_error.txt
#SBATCH --open-mode=truncate
#SBATCH --constraint=EPYC_7742

module restore
module load gcc/6.3.0 python ffmpeg
module list

lscpu

cd ../tools/

echo ""; echo "PLOT"; echo ""

python plot.py blast_part density 300
# python plot.py blast_part pressure 300

# python plot.py blast_ball density 300

cd ../run/