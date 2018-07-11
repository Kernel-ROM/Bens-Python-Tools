#!/usr/bin/env python
"""
Quick tool to mass check port 80 HTTP connectivity. Requires: tqdm, futures, requests & requests[security]
"""
import requests
import argparse
import logging
from concurrent.futures import ThreadPoolExecutor
import sys
from tqdm import tqdm


def do_thread_work(args):
    site_scan(args[0], args[1], args[2], args[3], args[4])


def main():

    default_timeout = 5
    default_threads = 20

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-t", "--timeout", help="timeout value (seconds) for each connection, default is 5",
                        nargs="?", const=1, type=int, default=default_timeout)
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

    if args.timeout:
        timeout = args.timeout
    else:
        timeout = default_timeout

    with open(args.infile) as f:
        domains = f.readlines()

    domains = [x.strip() for x in domains]  # Strip whitespace and newline chars
    domain_len = len(domains)

    output = [None] * domain_len
    out_file = open(args.outfile, 'w+')

    print "\nPreparing to connect to %s domains\n" % str(len(domains))

    pool = ThreadPoolExecutor(max_workers=args.threads)

    pbar = tqdm(total=domain_len, disable=bar_disable)

    for i in xrange(domain_len):
        args = [domains[i], timeout, pbar, i, output]
        pool.submit(do_thread_work, args)

    pool.shutdown(wait=True)

    for line in output[:-1]:
        for lines in line:
            out_file.write(lines)
        out_file.write("\n")
    for i in output[-1]:
        out_file.write(output[-1])
    # out_file.write(output[-1])

    print "\nFinished!"


def site_scan(url, t, pbar, index, output):

    logging.debug("Connecting to %s" % url)

    try:
        r = requests.get("http://" + url, timeout=t, allow_redirects=False)
        if r.status_code == 404:
            output[index] = "N - 404"
        else:
            output[index] = "Y - %s" % r.status_code
        logging.debug("%s: %s" % (url, str(r.status_code)))

    except requests.exceptions.Timeout:
        output[index] = "N - Timeout"
        logging.debug("%s: Timeout" % url)
        pass

    except requests.exceptions.ConnectionError:
        output[index] = "? - Connection Error"
        logging.debug("%s: Timeout" % url)
        pass

    except requests.exceptions.SSLError:
        try:
            r = requests.get("https://" + url, timeout=t, allow_redirects=False)
            if r.status_code == 404:
                output[index] = "N - 404"
            else:
                output[index] = "Y - %s" % r.status_code

            logging.debug("%s: %s" % (url, str(r.status_code)))

        except requests.exceptions.SSLError:
            output[index] = "? - SSL Error"
            logging.debug("%s: SSL Error" % url)
            pass

    except Exception as e:
        output[index] = "? - SSL Error"
        logging.debug("%s: SSL Error - %r" % (url, e))
        pass

    pbar.update(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
