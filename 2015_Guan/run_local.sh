#!/bin/bash
TIMEPATTERN=$( date +%Y_%m_%d_%H_%M_%S ) snakemake --config nprim=100  stop_time=00:01:00 -j24
