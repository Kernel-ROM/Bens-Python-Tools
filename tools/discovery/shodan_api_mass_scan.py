#!/usr/bin/env python
"""
Quick tool to mass check ips and domains against Shodan. Requires: tqdm, futures & shodan
"""
import sys
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import shodan
import time

SHODAN_API_KEY = "INSERT_KEY_HERE"


def do_thread_work(args):
    shodan_scan(args[0], args[1], args[2], args[3])


def main():

    default_threads = 1

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    #parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-T", "--threads", help="number of threads to run, default is 20",
                        nargs="?", const=1, type=int, default=default_threads)
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

    # output = [""] * domain_len
    # out_file = open(args.outfile, 'w+')

    output = ""

    print "\nPreparing to check %s hosts\n" % str(len(domains))

    pool = ThreadPoolExecutor(max_workers=args.threads)

    pbar = tqdm(total=domain_len, disable=bar_disable)

    for i in xrange(domain_len):
        args = [domains[i], pbar, i, output]
        pool.submit(do_thread_work, args)
        time.sleep(1)

    pool.shutdown(wait=True)

    # for line in output[:-1]:
    #     out_file.write(line)
    #     out_file.write("\n")
    # out_file.write(output[-1])

    print "\nFinished!"


def shodan_scan(i, pbar, index, output):

    api = shodan.Shodan(SHODAN_API_KEY)

    logging.debug("Checking Shodan for %s" % i)

    try:
        host = api.host(i)

        # Print general info
        tqdm.write("IP: %s\nOrganization: %s\nOperating System: %s\n" % (host['ip_str'], host.get('org', 'n/a'), host.get('os', 'n/a')))

        # Print all banners
        for item in host['data']:
                tqdm.write("Port: %s\nBanner: %s" % (item['port'], item['data']))

        tqdm.write("\n\n\n\n")

    except shodan.exception.APIError as e:
        logging.debug("ERROR: %r" % str(e))
        # output[index] = None
        pass

    pbar.update(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
