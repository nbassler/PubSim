#!/bin/bash
module load plgrid/tools/python/3.9
TIMEPATTERN=$( date +%Y_%m_%d_%H_%M_%S ) PATH=$PATH:$SCRATCH/shieldhit snakemake --config nprim=10000 --notemp --cluster-config cluster.yaml --immediate-submit --cluster './immediate_submit.py {dependencies}' -j 5000
