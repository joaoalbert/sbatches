#!/bin/bash -f

#SBATCH --job-name=hide_test
#SBATCH -p sequana_cpu_dev
#SBATCH -N1 -n1
#SBATCH --mem-per-cpu=7G
#SBATCH --time=00:20:00
#SBATCH -o /scratch/bingo/joao.barretos/hide_and_seek/resultados/TOD/teste/hide_test.out
#SBATCH -e /scratch/bingo/joao.barretos/hide_and_seek/resultados/TOD/teste/hide_test.err

source /scratch/bingo/joao.barretos/hide_and_seek/hide_venv/bin/activate

echo Time is `date`
echo Running on host `hostname`
echo Directory is `pwd`
echo Files are `ls`
echo This jobs runs on the following processors:
echo $SLURM_JOB_NODELIST

python3 /scratch/bingo/joao.barretos/hide_and_seek/hide-base/run_hide.py

echo Time is `date`

