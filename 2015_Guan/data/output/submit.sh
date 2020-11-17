#!/usr/bin/env bash

wdir=`pwd`  # present working directory

cd ${wdir}/wdir
for shdir in $(find . -mindepth 1 -maxdepth 1 -type d )
do
	cd $shdir
	echo $shdir
	# echo sbatch --array 0-16 rsshield.sh
	/home/fredrik/projects/PubSim/2000_Furusawa/data/output/shieldhit
	# echo sbatch ../../../../rsshield.sh
	cd ${wdir}/wdir
done
