#!/usr/bin/env python
"""
Quick tool to mass retrieve whois data. Requires: tqdm & pythonwhois
"""

import argparse
import sys
from Queue import Queue
from threading import Thread
from tqdm import tqdm
import logging
import pythonwhois


def do_thread_work(q):
    while True:
        args = q.get()
        whois(args[0], args[1], args[2], args[3])
        q.task_done()


def main():

    default_threads = 10

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-T", "--threads", help="number of threads to run, default is 10",
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

    output = [""] * domain_len
    out_file = open(args.outfile, 'w+')

    print "\nPreparing to make to %s domain WHOIS queries.\n" % str(len(domains))

    q = Queue(maxsize=0)

    for i in range(args.threads):
        worker = Thread(target=do_thread_work, args=(q,))
        worker.setDaemon(True)
        worker.start()

    pbar = tqdm(total=domain_len, disable=bar_disable)

    for i in xrange(domain_len):
        q.put([domains[i], pbar, i, output])

    q.join()

    for line in output[:-1]:
        out_file.write(line)
        out_file.write("\n")
    out_file.write(output[-1])

    print "\nFinished!"


def whois(url, pbar, index, output):

    whois_fields = ['creation_date', 'registrant', 'registrar', 'country', 'state', 'city']
    delimiter = "|"

    logging.debug("Retrieving WHOIS for %s" % url)

    # try:
    r = pythonwhois.get_whois(url)
    logging.debug(r)

    for attribute in whois_fields:
        try:
            if attribute == 'creation_date':
                if type(r[attribute]) == list:
                    output[index] += (r[attribute][0].strftime("%B %d, %Y") + delimiter)
                else:
                    output[index] += (r[attribute].strftime("%B %d, %Y") + delimiter)
            elif type(r[attribute]) == list:
                item = "".join(r[attribute])
                output[index] += (item + delimiter)
            else:
                output[index] += (r[attribute] + delimiter)
        except KeyError:
            logging.debug("WHOIS dict missing %s attribute" % attribute)
            output[index] += (delimiter)
            pass

    # except Exception as e:
    #     output[index] = "? - WHOIS Error"
    #     logging.debug("WHOIS Error @ %s: %s" % (url, str(e)))
    #     pass

    pbar.update(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
