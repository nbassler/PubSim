#!/bin/bash
INPUT_FILTER="H[W|T]*" TIMEPATTERN=$( date +%Y_%m_%d_%H_%M_%S ) snakemake --config nprim=1000 stop_time=00:01:00 pmma_samples=2 -j4
