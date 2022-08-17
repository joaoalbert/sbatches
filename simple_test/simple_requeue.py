import os
import time

sbatch_f = "/scratch/bingo/joao.barretos/hide_and_seek/sbatches/simple_test/sbatch_simple_test.srm"
n_simple_teste = "/scratch/bingo/joao.barretos/hide_and_seek/sbatches/simple_test/simple_test{}.srm"
squeue = "squeue -u joao.barretos -p cpu_dev"
sleep_time = 5
n_testes = 2
max_queue = 1

for n_teste in range(n_testes): 
    os.system("cp {} {}".format(sbatch_f, n_simple_teste.format(n_teste)))
    
for n_teste in range(n_testes):
    in_queue = len(os.popen(squeue).read().split("\n"))-2
    print("{} jobs in queue".format(in_queue))
    while in_queue>=max_queue:
        print("Waiting for space in queue...")
        time.sleep(sleep_time)
        in_queue = len(os.popen(squeue).read().split("\n"))-2
    print("Executing sbatch {}".format(n_teste))
    os.system("sbatch {}".format(n_simple_teste.format(n_teste)))
