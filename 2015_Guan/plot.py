#!/usr/bin/env python3

import argparse
import logging
import os
import sys

import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pylab as plt

logger = logging.getLogger(__name__)


def plot_results(input_file, output_file):
    df = pd.read_csv(input_file)
    df.sort_values(by=['stat_moment', 'ion', 'pmma'], inplace=True)
    df_mean = df[df.stat_moment == 'mean']
    df_stderr = df[df.stat_moment == 'stderr']

    ions = df.ion.unique()

    # plot as function of PMMA depth

    # Create the PdfPages object to which we will save the pages:
    # The with statement makes sure that the PdfPages object is closed properly at
    # the end of the block, even if an Exception occurs.
    if output_file.endswith('.pdf'):
        output_file_pdf = output_file
    else:
        output_file_pdf = output_file + '.pdf'
    with PdfPages(output_file_pdf) as pdf:

        for row_no in range(df.columns.size - 3):
            fig, axes = plt.subplots(nrows=1, ncols=df.ion.nunique(), figsize=(9, 5))

            for col_no, ax in enumerate(axes):
                x = df_mean[df_mean.ion == ions[col_no]].pmma
                y = df_mean[df_mean.ion == ions[col_no]][df_mean.columns[3 + row_no]].values
                ax.set_title("{}, {}".format(ions[col_no], df.columns[3 + row_no]), fontsize=8)
                ax.grid()
                if np.any(y):
                    y_err = df_stderr[df_stderr.ion == ions[col_no]][df_stderr.columns[3 + row_no]].values
                    ax.errorbar(x, y, y_err, fmt='.')
                else:
                    ax.plot(x, y, '.')

            if output_file.endswith('.pdf'):
                pdf.savefig(figure=fig)
            else:
                file_base, file_ext = os.path.splitext(output_file)
                fig.savefig(file_base + '_' + df.columns[3 + row_no] + file_ext)


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
