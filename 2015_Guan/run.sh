#!/bin/bash
# Submission script for embarrasingly parallel runs on a SLURM cluster.
#
#SBATCH --ntasks=2  # number of tasks should be consistent with contents of job.conf !
#SBATCH -p plgrid-short    # partitions with highest priorities: plgrid-short (prometheus), fast (eagle)
#SBATCH --time=00:14:00    # walltime, should be below 1 hour for highest priority
#SBATCH --output=shieldhitJob.%J.out     # standard output file name
#SBATCH --error=shieldhitJob.%J.err      # standard error output file name


echo Node ID       $SLURM_NODEID
echo NTasks        $SLURM_NTASKS
echo NNodes        $SLURM_NNODES
echo LocalID       $SLURM_LOCALID
echo Array task ID $SLURM_ARRAY_TASK_ID

# some clusters needs non-standard GCC (it should be compliant with gcc used to compile SH12A binary)
module load plgrid/tools/gcc/10.1.0  # prometheus
export PATH=$PATH:$SCRATCH/shieldhit/  # prometheus

# number of tasks should be consistent with --ntasks
# here you can also specify number of primaries for each task
cat > job.conf <<EOF
0-1 shieldhit --seedoffset=%t --nstat=5000
EOF

# run many parallel tasks using srun (probably around 100)
srun --multi-prog job.conf

