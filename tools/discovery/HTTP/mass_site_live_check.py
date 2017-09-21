#!/usr/bin/env python
"""
Quick tool to mass check port 80 HTTP connectivity. Requires: tqdm, requests, requests['security'] & dnspython
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
        args = q.get()
        site_scan(args[0], args[1], args[2], args[3])
        q.task_done()


def main():

    default_timeout = 5
    default_threads = 10

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-t", "--timeout", help="timeout value (seconds) for each connection, default is 5",
                        nargs="?", const=1, type=int, default=default_timeout)
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

    if args.timeout:
        timeout = args.timeout
    else:
        timeout = default_timeout

    with open(args.infile) as f:
        domains = f.readlines()

    domains = [x.strip() for x in domains]  # Strip whitespace and newline chars

    global output
    output = []

    out_file = open(args.outfile, 'w+')

    print "\nPreparing to connect to %s domains\n" % str(len(domains))

    q = Queue(maxsize=0)

    for i in range(args.threads):
        worker = Thread(target=do_stuff, args=(q,))
        worker.setDaemon(True)
        worker.start()

    pbar = tqdm(total=100, disable=bar_disable)

    increment = 100 / len(domains)

    for url in domains:
        q.put([url, timeout, pbar, increment])

    q.join()

    for line in output[:-1]:
        out_file.write(line)
        out_file.write("\n")
    out_file.write(output[-1])

    print "\nFinished!"


def site_scan(url, t, pbar, inc):

    logging.debug("Connecting to %s" % url)

    try:
        r = requests.get("http://" + url, timeout=t)
        if r.status_code == 404:
            output.append("N - 404")
        else:
            output.append("Y - %s" % r.status_code)
        logging.debug("%s: %s" % (url, str(r.status_code)))

    except requests.exceptions.Timeout:
        output.append("N - Timeout")
        logging.debug("%s: Timeout" % url)
        pass

    except requests.exceptions.ConnectionError:
        output.append("? - Connection Error")
        logging.debug("%s: Timeout" % url)
        pass

    except requests.exceptions.SSLError:
        try:
            r = requests.get("https://" + url, timeout=t)
            if r.status_code == 404:
                output.append("N - 404")
            else:
                output.append("Y - %s" % r.status_code)

            logging.debug("%s: %s" % (url, str(r.status_code)))

        except requests.exceptions.SSLError:
            output.append("? - SSL Error")
            logging.debug("%s: SSL Error" % url)
            pass

    pbar.update(inc)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
