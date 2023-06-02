#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=512
#SBATCH --time=01:00:00
#SBATCH --job-name=sod
#SBATCH --output=slurm/sod_output.txt
#SBATCH --error=slurm/sod_error.txt
#SBATCH --open-mode=truncate
#SBATCH --constraint=EPYC_7742

lscpu

# echo ""; echo "GENERATE"; echo ""
# module restore; module load gcc
# cd ../tools/; source generate.sh; cd ../run/

echo ""; echo "BUILD"; echo ""
module restore
# module load gcc/6.3.0 cmake cuda gsl openmpi hdf5 fftw openblas python ffmpeg
module load gcc/8.2.0 cmake cuda gsl openmpi hdf5 fftw openblas boost python
module list

export OMP_NUM_THREADS=16
cd ../build/; make; cd ../run/

echo ""; echo "START at "; date; echo ""

time srun ../build/pkdgrav3 cosmology_sod.par

echo ""; echo "END at "; date; echo ""

module restore
module load gcc/6.3.0 python ffmpeg
module list

echo ""; echo "PLOT"; echo ""

cd ../tools/

time python plot.py sod density 100
time python plot.py sod pressure 100

echo ""; echo "ANIMATE"; echo ""

time python animate.py sod 100

cd ../run/

echo ""; echo "DONE"; echo ""