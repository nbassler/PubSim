#!/usr/bin/env python3

import argparse
import logging
import sys

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pylab as plt

logger = logging.getLogger(__name__)


def plot_results(input_file, output_file):
    df = pd.read_csv(input_file)
    df.sort_values(by=['stat_moment', 'ion', 'pmma'], inplace=True)
    df_mean = df[df.stat_moment == 'mean']
    df_stderr = df[df.stat_moment == 'stderr']

    ions = df.ion.unique()
    no_of_filters = df.columns.size - 3

    # plot as function of PMMA depth
    fig, ax_table = plt.subplots(nrows=df.columns.size - 3, ncols=df.ion.nunique(), figsize=(9, no_of_filters * 5))
    for row_no, ax_row in enumerate(ax_table):
        for col_no, ax in enumerate(ax_row):
            x = df_mean[df_mean.ion == ions[col_no]].pmma
            y = df_mean[df_mean.ion == ions[col_no]][df_mean.columns[3 + row_no]].values
            y_err = df_stderr[df_stderr.ion == ions[col_no]][df_stderr.columns[3 + row_no]].values
            ax.set_title("{}, {}".format(ions[col_no], df.columns[3 + row_no]))
            if np.any(y):
                ax.errorbar(x, y, y_err, fmt='.')
            else:
                ax.plot(x, y, '.')

    fig.savefig(output_file)


def plot_benchmark(workspace_dir, output_file):
    pass


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help="path to summary file", default='summary.csv')
    parser.add_argument('output', type=str, help="path to output file", default='plot.svg')
    parser.add_argument('-v', '--verbosity', action='count', help="increase output verbosity", default=0)
    parsed_args = parser.parse_args(args)

    if parsed_args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif parsed_args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    plot_results(parsed_args.input, parsed_args.output)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
