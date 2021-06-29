#!/bin/bash
module load plgrid/tools/python/3.9
TIMEPATTERN=$( date +%Y_%m_%d_%H_%M_%S ) PATH=$PATH:$SCRATCH/shieldhit snakemake --config nprim=1000 stop_time=00:01:00 -j24
