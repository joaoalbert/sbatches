import os

horn_i, horn_f = 0, 28 # 0-28 ultimo nao incluso
day_i, day_f = 1, 5 # 1-5 ultimo incluso

# where local hide is:
local_hide = "/scratch/bingo/joao.barretos/hide_and_seek/HS_scripts/hide-beam/"
# where auto_run_hide.py is
ARH_FILE = "/scratch/bingo/joao.barretos/hide_and_seek/HS_scripts/auto_run_hide.py"
# where sbatch is
SBATCH_FILE = "/scratch/bingo/joao.barretos/hide_and_seek/sbatches/auto_jobs/sbatch_auto_jobs.srm"
new_sbatches = "/scratch/bingo/joao.barretos/hide_and_seek/sbatches/auto_jobs/sbatch_auto_jobs_{}.srm"


sbatch_cmd = "sbatch {}"
# command line to run hide
srun_cmd = "srun hide hide.config.{bingo} &\n"
cmd_landmark = "# Jobs go below\n"
n_perbatch = 10

sbatch_o_landmark = "#SBATCH -o "
sbatch_e_landmark = "#SBATCH -e "


source = os.path.join(local_hide, "hide", "config")
RH_FILE = os.path.join(local_hide, "run_hide.py")

base_file = os.path.join(source, "bingo.py")
perday_name_fmt = "bingo_day_{}.py"
perhorn_name_fmt = "bingo_day_{}_horn_{{}}"


bingo_files = []

for day in range(day_i, day_f+1):

	perday_name = perday_name_fmt.format(day)
	bingo_horn = perhorn_name_fmt.format(day)
	bingo_day = os.path.join(source, perday_name)
	
	# copia o bingo 5 vezes
	print("\n\nCriando {}...".format(perday_name))
	os.system("cp {} {}".format(base_file, bingo_day))
	
	# rodar o autorunhide 5 vezes pra gerar 5 bingos base com 5 dias diferentes
	print("\n\nAlterando data para dia {}...".format(day))
	os.system("python3 {script} {day} {config_file} {hide_path}".format(script=ARH_FILE, day=day, config_file=bingo_day, hide_path=local_hide))
	
	# rodar o runhide pra gerar 28 bingos pra cada dia
	print("\n\nCriando para as cornetas {}-{}...".format(horn_i, horn_f))
	os.system("python3 {script} {base_file} {new_files} {horn_i} {horn_f}".format(script=RH_FILE, base_file=perday_name, new_files=bingo_horn, horn_i=horn_i, horn_f=horn_f))
	
	for horn in range(horn_i,horn_f):
		perhorn_name = bingo_horn.format(horn)
		bingo_files.append(perhorn_name)#os.path.join(source, perhorn_name))


print("\n\nTotal de arquivos criados: {}".format(len(bingo_files)))
n_sbatches = len(bingo_files)//n_perbatch+1
print("Criando {} sbatches com {} jobs cada...".format(n_sbatches, n_perbatch))

with open(SBATCH_FILE, "r") as sbatch_open:
	sbatch_lines = sbatch_open.readlines()
	for i, sbatch_line in enumerate(sbatch_lines):
		if sbatch_line.startswith(sbatch_o_landmark):
			sbatch_o_line = i
		elif sbatch_line.startswith(sbatch_e_landmark):
			sbatch_e_line = i
		elif sbatch_line.startswith(cmd_landmark):
			start_from = i
			break
			
			
# Criar novos sbatches
for n_sbatch in range(n_sbatches):

	new_sbatch = new_sbatches.format(n_sbatch)
	new_sbatch_lines = sbatch_lines.copy()
	if n_sbatch==n_sbatches-1:
		n_perbatch = len(bingo_files)%n_perbatch
	
	with open(new_sbatch,"w") as new_sbatchf:
		for n_srun in range(n_perbatch):
		
			err_out_file = new_sbatch.split(".")[0]
			new_sbatch_lines[sbatch_o_line] = sbatch_o_landmark + err_out_file + ".out\n"
			new_sbatch_lines[sbatch_e_line] = sbatch_e_landmark + err_out_file + ".err\n"
			
			bingo_i = n_sbatch*n_perbatch+n_srun
			bingof = bingo_files[bingo_i]
			n_srun_cmd = srun_cmd.format(bingo=bingof)		
			new_sbatch_lines.insert(start_from+n_srun+1, n_srun_cmd)
	
		new_sbatchf.writelines(new_sbatch_lines)
			
	# enviar diversos sbatches de uma vez para fila cpu_shared
	#os.system(sbatch_cmd.format(new_sbatch))

