#!/usr/bin/env python
"""
Tool to perform mass havibeenpwnd.com API queries. Requires: tqdm & requests
"""
import requests
import argparse
import sys
import json
import time
from pprint import pprint
import logging
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-s", "--sleep", help="""value in seconds to delay each connection 
                        to prevent rate-limiting, default is 1.5""",
                        nargs="?", const=1, type=int, default=1.5)
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
        emails = f.readlines()

    emails = [x.strip() for x in emails]  # Strip whitespace and newline chars

    print "Preparing to check %s emails\n\n" % str(len(emails))

    with open(args.outfile, 'w+') as out_file:

        for i in tqdm(emails, disable=bar_disable):
            try:
                result = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/' + i, timeout=5)
                out_file.write("Breach results for %s:\n" % i)
                pprint((json.loads(result.text.encode("utf-8"))), stream=out_file, indent=4)
                out_file.write("\n\n\n\n")

            except ValueError:
                out_file.write("No breach results for %s" % i)
                out_file.write("\n\n\n\n")
                continue

            time.sleep(args.sleep)

    print "\nFinished!"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
