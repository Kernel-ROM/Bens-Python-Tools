#!/usr/bin/env python
"""
Tool to perform mass DNS record queries. Requires: tqdm & dnspython
Doesn't seem to work with SPF records...
"""
import sys
import logging
import argparse
from Queue import Queue
from threading import Thread
import dns.resolver
from tqdm import tqdm


def do_thread_work(q):
    while True:
        args = q.get()
        resolver(args[0], args[1], args[2], args[3], args[4], args[5])
        q.task_done()


def main():

    default_threads = 10
    default_dns_server = "8.8.8.8"

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    parser.add_argument("-r", "--record-type", help="DNS record type to search for", required=True)
    parser.add_argument("-t", "--threads", help="number of threads to run, default is 10",
                        nargs="?", const=1, type=int, default=default_threads)
    parser.add_argument("-s", "--server", help="DNS server to query, default is 8.8.8.8",
                        nargs="?", default=default_dns_server)
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

    print "Preparing to resolve %s %s records\n\n" % (str(len(domains)), args.record_type)

    my_resolver = dns.resolver.Resolver()
    my_resolver.nameservers = [args.server]

    q = Queue(maxsize=0)

    for i in range(args.threads):
        worker = Thread(target=do_thread_work, args=(q,))
        worker.setDaemon(True)
        worker.start()

    pbar = tqdm(total=domain_len, disable=bar_disable)

    for i in xrange(domain_len):
        q.put([domains[i], pbar, args.record_type, i, output, my_resolver])

    q.join()

    for line in output[:-1]:
        out_file.write(line)
        out_file.write("\n")
    out_file.write(output[-1])

    print "\nFinished!"


def resolver(host, pbar, record_type, index, output, dns_resolver):

    logging.debug("Resolving DNS %s record for %s" % (record_type, host))
    try:
        answers = dns_resolver.query(host, record_type)
        for j in xrange(len(answers)):
            if (len(answers) > 1) & (j != len(answers) - 1):
                output[index] += "%s, " % str(answers[j])
            else:
                output[index] += "%s " % str(answers[j])

    except dns.resolver.NoAnswer:
        logging.debug("Error: No Answer")
        output[index] += "N/A - No Answer"
        pass
    except dns.resolver.NoNameservers:
        logging.debug("Error: No Nameservers Found")
        output[index] += "N/A - No Nameservers Found"
        pass
    except dns.resolver.NXDOMAIN:
        logging.debug("Error: None-existant Domain")
        output[index] += "N/A - Non-existent Domain"
        pass
    except dns.exception.Timeout:
        logging.debug("Error: DNS Timeout")
        output[index] += "N/A - DNS Timeout"
        pass

    pbar.update(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
