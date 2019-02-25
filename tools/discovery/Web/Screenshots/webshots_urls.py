#!/usr/bin/env python
"""
Quick tool to take a file of urlsand use wkhtmltoimage.exe to take screenshots - benl@modux.co.uk

Requires tqdm

Note: If possible use the webshots_xml_nmap.py script instead for better results.
"""
import sys
import os
import argparse
import subprocess
from Queue import Queue
from threading import Thread
from tqdm import tqdm

http_prefixes = ["http", "https"]

wkhtmltoimage_location = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe"

default_threads = 10


def main():

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outdir", help="output directory", required=True)
    parser.add_argument("-t", "--threads", help="number of threads to run, default is 10",
                        nargs="?", const=1, type=int, default=default_threads)
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    with open(args.infile, "r") as file:
        hosts = file.readlines()

    host_count = len(hosts)

    print "\nPreparing to screenshot %s hosts\n" % str(host_count)

    pbar = tqdm(total=host_count, disable=args.verbose)

    q = Queue(maxsize=0)

    for i in range(args.threads):
        worker = Thread(target=do_thread_work, args=(q,))
        worker.setDaemon(True)
        worker.start()

    for host in hosts:
        q.put([host, args.outdir, pbar, args.verbose])

    q.join()

    print "\nFinished!"


def do_thread_work(q):
    while True:
        args = q.get()
        webshot(args[0], args[1], args[2], args[3])
        q.task_done()


def webshot(host, outdir, pbar, verbose):
    null_out = open(os.devnull, 'w')
    for prefix in http_prefixes:
        url = prefix + "://" + host
        filename = prefix + "_" + host + "_" + ".png"
        path = os.path.join(outdir, filename)
        if verbose:
            subprocess.call([wkhtmltoimage_location, url, path])
        else:
            subprocess.call([wkhtmltoimage_location, url, path], stdout=null_out, stderr=subprocess.STDOUT)
    pbar.update(1)
    return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
