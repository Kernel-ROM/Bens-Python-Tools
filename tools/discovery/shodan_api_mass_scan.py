#!/usr/bin/env python
"""
Quick tool to mass check ips and domains against Shodan. Requires: tqdm & shodan
"""
import sys
import argparse
import logging
from tqdm import tqdm
import shodan
import time

SHODAN_API_KEY = ""


def main():

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-d", "--delay", help="delay between requests", default=1)
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

    with open(args.infile) as f:
        domains = f.readlines()

    domains = [x.strip() for x in domains]  # Strip whitespace and newline chars
    domain_len = len(domains)

    out_file = open(args.outfile, 'w+')

    print "\nPreparing to check %s hosts\n" % str(len(domains))

    pbar = tqdm(total=domain_len, disable=bar_disable)

    for i in xrange(domain_len):
        shodan_scan(domains[i], pbar, i, out_file, float(args.delay))

    print "\nFinished!"

    out_file.close()


def shodan_scan(i, pbar, index, out_file, delay):

    api = shodan.Shodan(SHODAN_API_KEY)

    logging.debug("Checking %s..." % i)

    out_file.write("Results for %s:\n" % i)

    try:

        time.sleep(delay)

        host = api.host(i)

        # Print general info
        out_file.write("IP: %s\nOrganization: %s\nOperating System: %s\n" % (host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))

        # Print all banners
        for item in host['data']:
                out_file.write("Port: %s\nBanner: %s" % (item['port'], item['data'].encode('utf-8')))

        out_file.write("\n###############################################################\n")

    except shodan.exception.APIError as e:
        logging.debug("ERROR: %r" % str(e))
        out_file.write(str(e))
        out_file.write("\n###############################################################\n")
        pass

    pbar.update(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
