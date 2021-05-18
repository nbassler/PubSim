#!/bin/bash

# create dedicated directory for each submission
TIMEPATTERN=$( date +%Y_%m_%d_%H_%M_%S )
WORKSPACE=${WORKSPACE_ENV:-workspace}_${TIMEPATTERN}
mkdir $WORKSPACE

# copy contents of original directory, dereferencing all links
# for bookkeeping it is better solution as files to which links are pointing may change after submission
cp -rL data/output/wdir/* $WORKSPACE

find $WORKSPACE -type d -exec cp run.sh {} \;
find $WORKSPACE -type d -exec cp job.conf {} \;

# find all subdirectories containing beam.dat file and submit jobs from there
find $WORKSPACE -name beam.dat -execdir sbatch run.sh \;
