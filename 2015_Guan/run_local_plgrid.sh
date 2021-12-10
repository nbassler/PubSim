#!/bin/bash
module load plgrid/tools/python/3.9
source ./venv/bin/activate
INPUT_FILTER="H[W|T]*" TIMEPATTERN=$( date +%Y_%m_%d_%H_%M_%S ) PATH=$PATH:$SCRATCH/shieldhit snakemake --config nprim=10000 stop_time=00:01:00 pmma_samples=2 -j24
