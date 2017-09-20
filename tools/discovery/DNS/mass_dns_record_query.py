#!/usr/bin/env python
"""
Tool to perform mass DNS record queries. Requires: tqdm & dnspython
"""
import dns.resolver
import argparse
import logging
import sys
from tqdm import tqdm


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-r", "--record-type", help="DNS record type to search for", required=True)
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

    out_file = open(args.outfile, 'w+')

    print "Preparing to resolve %s %s records\n\n" % (str(len(domains)), args.record_type)

    for i in tqdm(domains, disable=bar_disable):
        print i, len(i)
        logging.debug("Resolving DNS %s record for %s" % (args.record_type, i))
        try:
            answers = dns.resolver.query(i, args.record_type)
            for j in xrange(len(answers)):
                if (len(answers) > 1) & (j != len(answers) - 1):
                    out_file.write("%s, " % str(answers[j])[:-1])
                else:
                    out_file.write("%s " % str(answers[j])[:-1])

        except dns.resolver.NoAnswer:
            logging.debug("Error: No Answer")
            out_file.write("N/A - No Answer")
            pass
        except dns.resolver.NoNameservers:
            logging.debug("Error: No Nameservers Found")
            out_file.write("N/A - No Nameservers Found")
            pass
        except dns.resolver.NXDOMAIN:
            logging.debug("Error: None-existant Domain")
            out_file.write("N/A - Non-existent Domain")
            pass
        except dns.exception.Timeout:
            logging.debug("Error: DNS Timeout")
            out_file.write("N/A - DNS Timeout")
            pass

        out_file.write("\n")

    print "\nFinished!"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
