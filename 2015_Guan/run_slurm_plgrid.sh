#!/bin/bash
module load plgrid/tools/python/3.9
source ./venv/bin/activate
INPUT_FILTER="H[W|T]*" TIMEPATTERN=$( date +%Y_%m_%d_%H_%M_%S ) PATH=$PATH:$SCRATCH/shieldhit snakemake --config nprim=100000000  stop_time=00:30:00 --notemp --cluster-config plgrid_cluster_conf.yaml --immediate-submit --cluster './submit_snake_slurm.py {dependencies}' -j 5000
