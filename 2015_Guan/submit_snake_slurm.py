#!/usr/bin/env python3
import os
import sys

from snakemake.utils import read_job_properties

# last command-line argument is the job script
jobscript = sys.argv[-1]

# all other command-line arguments are the dependencies
dependencies = set(sys.argv[1:-1])

# parse the job script for the job properties that are encoded by snakemake within
job_properties = read_job_properties(jobscript)
print(job_properties["wildcards"])

# collect all command-line options in an array
cmdline = ["sbatch"]

# set all the slurm submit options as before
slurm_args = " -p {partition} -n {ntasks} -t {time} -J {job-name} ".format(**job_properties["cluster"])

if 'workspace' in job_properties["wildcards"]:
    workspace = job_properties["wildcards"]["workspace"]
    os.makedirs(workspace, exist_ok=True)
    os.makedirs(workspace + "/logs", exist_ok=True)
    slurm_args += "-o {workspace}/logs/slurm-%j-%x.err -e {workspace}/logs/slurm-%j-%x.out ".format(workspace=workspace)
cmdline.append(slurm_args)

if dependencies:
    cmdline.append("--dependency")
    # only keep numbers in dependencies list
    dependencies = [x for x in dependencies if x.isdigit()]
    cmdline.append("afterok:" + ",".join(dependencies))

cmdline.append(jobscript)

os.system(" ".join(cmdline))
