#!/usr/bin/env python

import argparse
import json
from collections import OrderedDict
import logging
import os
import sys

from pymchelper.estimator import ErrorEstimate
from pymchelper.input_output import frompattern

logger = logging.getLogger(__name__)


def save_summary_file(estimator, output_dir, output_suffix="all.dat"):
    estimator_corename = estimator.file_corename.rstrip('_')
    output_file_name = os.path.join(output_dir, estimator_corename + output_suffix)
    logger.info("Saving data into {}".format(output_file_name))
    with open(output_file_name, "w") as output_file:
        # write column names
        for page in estimator.pages:
            output_file.write("{},{} ".format(page.name, page.page_filter_name))
        output_file.write('\n')

        # write mean values
        for page in estimator.pages:
            output_file.write("{} ".format(page.data[0, 0, 0, 0, 0]))
        output_file.write('\n')

        # write standard error values
        for page in estimator.pages:
            output_file.write("{} ".format(page.error[0, 0, 0, 0, 0]))
        output_file.write('\n')


def save_metadata_file(estimator, file_path):
    d = OrderedDict()
    for main_attr_name in sorted(estimator.__dict__.keys(), key=lambda x: x[0].lower()):
        if main_attr_name == 'pages':
            d[main_attr_name] = []
            for page in estimator.pages:
                page_dict = OrderedDict()
                for page_attr_name in sorted(page.__dict__.keys(), key=lambda x: x[0].lower()):
                    if page_attr_name not in ('estimator', 'data_raw', 'error_raw'):
                        page_dict[page_attr_name] = str(page.__dict__[page_attr_name])
                d[main_attr_name].append(page_dict)
        else:
            d[main_attr_name] = str(estimator.__dict__[main_attr_name])
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=4)


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help="path to BDO files", default='.')
    parser.add_argument('output', type=str, help="directory where output should be saved", default='.')
    parser.add_argument('-v', '--verbosity', action='count', help="increase output verbosity", default=0)
    parsed_args = parser.parse_args(args)

    if parsed_args.verbosity == 1:
        logging.basicConfig(level=logging.INFO)
    elif parsed_args.verbosity > 1:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig()

    bdo_path = os.path.join(parsed_args.input, '*.bdo')
    logger.info("Reading from path {}".format(bdo_path))

    estimators = frompattern(bdo_path, error=ErrorEstimate.stderr, nan=False)
    for estimator in estimators:
        save_summary_file(estimator, parsed_args.output, output_suffix="all_with_nan.dat")

    estimators = frompattern(bdo_path, error=ErrorEstimate.stderr, nan=True)
    for estimator in estimators:
        save_summary_file(estimator, parsed_args.output, output_suffix="all_excluding_nan.dat")


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

