#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from glob import iglob
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def merge_files(workspace_dir, datafile_pattern, output_file):
    logger.info("Reading from path {}".format(workspace_dir))

    logger.info("Looking for files {}".format(datafile_pattern))

    dir_glob = os.path.join(workspace_dir, '*', '*_*', datafile_pattern)
    # list of files matching pattern
    file_list = [f for f in iglob(dir_glob, recursive=True) if os.path.isfile(f)]
    logger.info("Discovered {} files matching pattern".format(len(file_list)))
    logger.info("Discovered files: {} , ...".format(", ".join(file_list[0:3])))

    dataframes = []
    for datafile in file_list:
        # extract ion type and thickness from directory name
        ion_pmma_part = Path(datafile).parts[-2]
        ion = ion_pmma_part.split('_')[0]
        pmma = float(ion_pmma_part.split('_')[1])

        logger.debug("Ion {}, PMMA thickness {}".format(ion, pmma))

        # read mean values and standard errors
        df = pd.read_csv(datafile, delim_whitespace=True)
        df.insert(0, 'stat_moment', 'mean')
        df.loc[1, 'stat_moment'] = 'stderr'
        df.insert(1, 'ion', ion)
        df.insert(2, 'pmma', pmma)

        dataframes.append(df)

    # construct pandas dataframe from the datafiles
    df = pd.concat(dataframes)

    # dump dataframe to CSV file
    df.to_csv(output_file, index=False, columns=dataframes[0].columns)


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help="path to workspace directory", default='.')
    parser.add_argument('output', type=str, help="directory where output should be saved", default='.')
    parser.add_argument('--pattern', type=str, help="summary file filename or pattern",
                        default='bin_data_all_with_nan.dat')
    parser.add_argument('-v', '--verbosity', action='count', help="increase output verbosity", default=0)
    parsed_args = parser.parse_args(args)

    if parsed_args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif parsed_args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    merge_files(parsed_args.input, parsed_args.pattern, parsed_args.output)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
