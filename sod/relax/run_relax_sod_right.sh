#!/bin/bash

#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --mem-per-cpu=512
#SBATCH --time=02:00:00
#SBATCH --job-name=relax_sod_right
#SBATCH --output=slurm/relax_sod_right_output.txt
#SBATCH --error=slurm/relax_sod_right_error.txt
#SBATCH --open-mode=truncate
#SBATCH --constraint=EPYC_7742

lscpu
module restore
# module load gcc/6.3.0 cmake cuda gsl openmpi hdf5 fftw openblas python ffmpeg
module load gcc/8.2.0 cmake cuda gsl openmpi hdf5 fftw openblas boost python
module list

echo ""; echo "BUILD"; echo ""

export OMP_NUM_THREADS=16
cd ../build/; make; cd ../run/

echo ""; echo "START at "; date; echo ""

time srun ../build/pkdgrav3 cosmology_relax_sod_right.par

echo ""; echo "END at "; date; echo ""

cp /cluster/scratch/ariess/relax_sod_right/relax_sod_right.01600 ./sod_ic_grid_isentrope_right_relaxed1600.tipsy

module restore
module load gcc/6.3.0 python ffmpeg
module list

cd ../tools/

echo ""; echo "ANIMATE"; echo ""

time python animate.py relax_sod_right 1600

echo ""; echo "DONE"; echo ""