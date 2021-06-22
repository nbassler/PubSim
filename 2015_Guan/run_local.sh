#!/bin/bash
TIMEPATTERN=$( date +%Y_%m_%d_%H_%M_%S ) snakemake --config nprim=1 -j24
