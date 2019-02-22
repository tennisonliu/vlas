#job creator py
import subprocess
with open("job.sh",'w') as f:
	f.write("#!/bin/bash")
	f.write("\n")

	f.write("#SBATCH --job-name=TWD\n")
	f.write("#SBATCH --time=10:00:00\n")
	f.write("#SBATCH --nodes=1\n")
	f.write("#SBATCH --cpus-per-task=1\n")
	f.write("#SBATCH --ntasks-per-node=1\n")
	f.write("#SBATCH --mem=100gb\n")
	f.write("#SBATCH --gres=gpu:4\n")

	f.write("date\n")
	f.write("source /home/liu181/Desktop/twd_HPC/job_prep.sh\n")
	f.write("date\n")
	f.write("python /home/liu181/Desktop/twd_HPC/twd_transfertraining.py\n")
	f.write("date\n")
subprocess.call(["sbatch", "job.sh"])