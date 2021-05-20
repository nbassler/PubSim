#!/usr/bin/env python

import argparse
import logging
import os
import sys
from glob import iglob
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


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

    workspace_dir = parsed_args.input
    logger.info("Reading from path {}".format(workspace_dir))

    datafile_pattern = parsed_args.pattern
    logger.info("Looking for files {}".format(datafile_pattern))

    dir_glob = os.path.join(workspace_dir, '*_*', datafile_pattern)
    # list of files matching pattern
    file_list = [f for f in iglob(dir_glob, recursive=True) if os.path.isfile(f)]
    logger.info("Discovered {} files matching pattern".format(len(file_list)))
    logger.info("Discovered files: {} , ...".format(", ".join(file_list[0:3])))

    data_as_list_of_lists = []
    for datafile in file_list:
        # extract ion type and thickness from directory name
        ion_thickness_part = Path(datafile).parts[-2]
        ion = ion_thickness_part.split('_')[0]
        thickness = float(ion_thickness_part.split('_')[1])

        # read mean values and standard errors
        mean_values, stderr_values = np.genfromtxt(datafile).tolist()

        # append to temporary datas tructure, including metadata read from dir name
        data_as_list_of_lists.append(['mean', ion, thickness, *mean_values])
        data_as_list_of_lists.append(['stderr', ion, thickness, *stderr_values])

    # construct pandas dataframe from the datafiles
    df = pd.DataFrame.from_records(data=data_as_list_of_lists)
    df.rename(columns={0: 'stat_moment', 1: 'ion', 2: 'thickness'}, inplace=True)
    if parsed_args.verbosity:
        print(df.head())

    # dump dataframe to CSV file
    df.to_csv(parsed_args.output, index=False)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

