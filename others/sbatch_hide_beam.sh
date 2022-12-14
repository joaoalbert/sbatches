#!/bin/bash -f

#SBATCH --job-name=hide_test
#SBATCH -p sequana_cpu_dev
#SBATCH -N1 -n1
#SBATCH --mem-per-cpu=7G
#SBATCH --time=00:20:00
#SBATCH -o /scratch/bingo/joao.barretos/hide_and_seek/resultados/TOD/zernike_150_MINUS110_nearest/hide_zernike_110_nearest.out
#SBATCH -e /scratch/bingo/joao.barretos/hide_and_seek/resultados/TOD/zernike_150_MINUS110_nearest/hide_zernike_110_nearest.err

source /scratch/bingo/joao.barretos/hide_and_seek/hide_beam_venv/bin/activate

cd /scratch/bingo/joao.barretos/hide_and_seek/hide-beam/

echo Time is `date`
echo Running on host `hostname`
echo Directory is `pwd`
echo Files are `ls`
echo This jobs runs on the following processors:
echo $SLURM_JOB_NODELIST

srun python3 run_hide.py

echo Time is `date`

