#!/usr/bin/env python
"""
Quick tool to take a nmap xml file and use wkhtmltoimage.exe to take screenshots - benl@modux.co.uk

nmap -p 80,443,8080,8000,8443,4443,593,5000,5800,8008,8888,8800 -Pn -n --reason -oA http_scan -iL

Requires python-libnmap & tqdm

Does not support IP based scans as of yet - Ben
"""
import sys
import os
import argparse
import subprocess
from Queue import Queue
from threading import Thread
from tqdm import tqdm
from libnmap.parser import NmapParser

https_ports = ["443", "8443", "4443"]

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

    nmap_report = NmapParser.parse_fromfile(args.infile)

    host_count = 0
    for host in nmap_report.hosts:
        if len(host.get_open_ports()):
            host_count += 1

    print "\nPreparing to screenshot %s hosts\n" % str(host_count)

    pbar = tqdm(total=host_count, disable=args.verbose)

    q = Queue(maxsize=0)

    for i in range(args.threads):
        worker = Thread(target=do_thread_work, args=(q,))
        worker.setDaemon(True)
        worker.start()

    for host in nmap_report.hosts:
        if host.ipv4:
            q.put([host, args.outdir, pbar, args.verbose, host.ipv4])
        elif host.hostnames:
            for hostname in host.hostnames:
                q.put([host, args.outdir, pbar, args.verbose, hostname])

    q.join()

    print "\nFinished!"


def do_thread_work(q):
    while True:
        args = q.get()
        webshot(args[0], args[1], args[2], args[3], args[4])
        q.task_done()


def webshot(host, outdir, pbar, verbose, hostname):
    null_out = open(os.devnull, 'w')
    if len(host.get_open_ports()):
        ports = host.get_open_ports()
        for port_tuple in ports:
            port = str(port_tuple[0])
            if port in https_ports:
                prefix = "https://"
            else:
                prefix = "http://"
            url = prefix + hostname + ":" + port
            filename = hostname + "_" + port + ".png"
            path = os.path.join(outdir, filename)
            if verbose:
                subprocess.call([wkhtmltoimage_location, "--disable-local-file-access", url, path])
            else:
                subprocess.call([wkhtmltoimage_location, "--disable-local-file-access", url, path], stdout=null_out, stderr=subprocess.STDOUT)

        pbar.update(1)
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
