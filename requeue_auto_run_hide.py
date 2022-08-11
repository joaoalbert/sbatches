import os
import time


rhPath = "/scratch/bingo/joao.barretos/hide_and_seek/hide-beam/run_hide.py" # run_hide -> horns
arhPath = "/scratch/bingo/joao.barretos/hide_and_seek/HS_scripts/auto_run_hide.py" # auto_run_hide -> days
#outPath = ""
batchPath = "/scratch/bingo/joao.barretos/hide_and_seek/sbatches/sbatch_auto_hide.sh"
squeue = "squeue -u joao.barretos | grep auto_hide"


horns_i, horns_f = 3, 27 #0-27
days_i, days_f = 1, 5 #1-30

# this must match what bingo.py says
obs_year = "2018"
obs_month = "01"

############################################################

#LAST_FILE_FMT = "bingo_tod_horn_{horn}_201801{dd:02d}_230000.h5"
SLEEP_TIME = 60  # cyclic time to check if run is over (seconds)

RH_LINE = "initial_horn, final_horn"
ARH_LINE = "	initial_day, final_day"

run = 1
N = (horns_f-horns_i)*(days_f-days_i)

sbatch = "sbatch {}".format(batchPath)


############################################################

def change_one_line(fpath, starts_with, change_to):
	with open(fpath, "w") as fopen:
		fline = fopen.readline()
		if fline.startswith(starts_with):
			fopen.write(change_to)
		else:
			fopen.write(fline)


############################################################

start = str(time.ctime())
print("Start time at {}\n".format(start))
        
for horn in range(horns_i, horns_f+1):

	# Change run_hide file
	rh_newline = RH_LINE + " = {}, {}\n".format(horn, horn+1)
	change_one_line(rhPath, RH_LINE, rh_newline)

	for day in range(days_i, days_f+1):
	
        print('\n\nRunning horn {} day {} ({}/{} run)'.format(horn, day, run, N))
        print("Run time: {}".format(time.ctime()))
        
        # Change auto_run_hide file
        arh_newline = ARH_LINE + " = {}, {}".format(day, day+1)
        change_one_line(arhPath, ARH_LINE, arh_newline)
        
        # Run sbatch
        os.system(sbatch)
        
        # Keep waiting while batch is in the queue
        while os.popen(squeue).read()!="": 
            print('Still running...')
        	time.sleep(SLEEP_TIME)
        	
        print("End of run {}. Requeuing next...".format(run))
        run += 1
            	
