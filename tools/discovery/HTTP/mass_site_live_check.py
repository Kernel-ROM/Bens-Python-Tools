#!/usr/bin/env python
"""
Quick tool to mass check port 80 HTTP connectivity. Requires: tqdm, requests & dnspython
TODO: Fix Threading
"""
import requests
import argparse
import logging
from Queue import Queue
from threading import Thread
import sys
from tqdm import tqdm


def do_stuff(q):
    while True:
        q.get()
        q.task_done()


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-t", "--timeout", help="timeout value (seconds) for each connection, default is 5",
                        nargs="?", const=1, type=int, default=5)
    parser.add_argument("-T", "--threads", help="number of threads to run, default is 10",
                        nargs="?", const=1, type=int, default=10)
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

    global domains
    domains = [x.strip() for x in domains]  # Strip whitespace and newline chars

    domains_ = domains * 1 # Easy way of making a static copy for iteration purposes

    global output
    output = []

    out_file = open(args.outfile, 'w+')

    print "Preparing to connect to %s domains\n\n" % str(len(domains))

    q = Queue(maxsize=0)

    for i in range(args.threads):
        worker = Thread(target=do_stuff, args=(q,))
        worker.setDaemon(True)
        worker.start()

    for j in tqdm(domains_, disable=bar_disable):
        q.put(site_scan(args.timeout))

    for line in output[:-1]:
        out_file.write(line)
        out_file.write("\n")
    out_file.write(output[-1])

    print "\nFinished!"


def site_scan(t):

    i = domains.pop(0)

    logging.debug("Connecting to %s" % i)

    try:
        r = requests.get("http://" + i, timeout=t)
        if r.status_code == 404:
            output.append("N - 404")
        else:
            output.append("Y - %s" % r.status_code)
        logging.debug("%s: %s" % (i, str(r.status_code)))

    except requests.exceptions.Timeout:
        output.append("N - Timeout")
        logging.debug("%s: Timeout" % i)
        pass

    except requests.exceptions.ConnectionError:
        output.append("? - Connection Error")
        logging.debug("%s: Timeout" % i)
        pass

    except requests.exceptions.SSLError:
        try:
            r = requests.get("https://" + i, timeout=t)
            if r.status_code == 404:
                output.append("N - 404")
            else:
                output.append("Y - %s" % r.status_code)

            logging.debug("%s: %s" % (i, str(r.status_code)))

        except requests.exceptions.SSLError:
            output.append("? - SSL Error")
            logging.debug("%s: SSL Error" % i)
            pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
