#!/usr/bin/env python
"""
Quick tool to mass check ips against CIDR ranges. Outputs two files that contain unique ips inside and outside of the ranges.
Requires: tqdm & netaddr
"""
import sys
import argparse
import logging
from tqdm import tqdm
from netaddr import IPNetwork, IPAddress


def main():

    outfile_inside_name = "internal"
    outfile_outside_name = "external"

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--ips", help="ip input file name", required=True)
    parser.add_argument("-r", "--ranges", help="ip range input file name", required=True)
    parser.add_argument("-s", "--state", help="optional internal/external output file name")
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                        action="store_true")
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    bar_disable = False

    if args.verbose:
        bar_disable = True
        logging.basicConfig(level=logging.DEBUG)

    with open(args.ips) as f:
        ips = f.readlines()

    with open(args.ranges) as f:
        ranges = f.readlines()

    ips = [x.strip() for x in ips]  # Strip whitespace and newline chars
    ranges = [x.strip() for x in ranges]  # Strip whitespace and newline chars
    ips_len = len(ips)
    ranges_len = len(ranges)

    inside_ips = []
    outside_ips = []
    state_output = [""] * ips_len

    filename = args.ips.split(".")
    base_file_name = filename[0]  # Retrieve input filename without extension (if exists)
    try:
        base_file_ext = "." + filename[1]
    except IndexError:
        base_file_ext = ".txt"

    outfile_inside = open(base_file_name + outfile_inside_name + base_file_ext, 'w+')
    outfile_outside = open(base_file_name + outfile_outside_name + base_file_ext, 'w+')

    print "\nPreparing to check %s ips against %s ranges\n" % (str(ips_len), str(ranges_len))

    pbar = tqdm(total=ips_len, disable=bar_disable)

    for i in xrange(ips_len):
        ip_range_check(ips[i], i, inside_ips, outside_ips, state_output, ranges)
        pbar.update(1)

    if args.state:
        out_file_state = open(args.state, 'w+')
        outfile_writer(out_file_state, state_output)

    outfile_writer(outfile_inside, inside_ips)
    outfile_writer(outfile_outside, outside_ips)


def outfile_writer(file, content):
    if len(content) > 0:
        for line in content[:-1]:
            file.write(line)
            file.write("\n")
        file.write(content[-1])


def ip_range_check(i, index, inside, outside, state_output, ranges):

    logging.debug("Checking %s" % i)

# hack to work with csv
    if "," in i:
        i_tmp = i.split(",")
        i = i_tmp[0]

    for j in ranges:
        if i in inside:
            state_output[index] = "Internal"
            break
        elif IPAddress(i) in IPNetwork(j):
            logging.debug("Found %s inside %s" % (i, j))
            inside.append(i)
            state_output[index] = "Internal"

    if i not in inside:
        outside.append(i)
        state_output[index] = "External"
        logging.debug("%s not found in any ranges" % i)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
