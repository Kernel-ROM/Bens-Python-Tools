#!/usr/bin/env python
"""
Quick tool to mass pull the Common Name and Subject Alt Names from SSL certs. Requires: tqdm, pyOpenSSL & dnspython
"""
import ssl
import sys
from socket import *
import argparse
from concurrent.futures import ThreadPoolExecutor
import logging
from tqdm import tqdm
import OpenSSL

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


def do_thread_work(args):
    cert_scan(args[0], args[1], args[2], args[3])


def main():

    default_threads = 20

    setdefaulttimeout(3)

    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
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

    output = [""] * domain_len
    out_file = open(args.outfile, 'w+')

    print "Preparing to analyse %s certs\n\n" % str(len(domains))

    pbar = tqdm(total=domain_len, disable=bar_disable)

    with ThreadPoolExecutor(max_workers=args.threads) as e:
        for i in xrange(domain_len):
            args = [domains[i], pbar, i, output]
            e.submit(do_thread_work, args)

    for line in output[:-1]:
        out_file.write(line)
        out_file.write("\n")
    out_file.write(output[-1])

    print "\nFinished!"


def cert_scan(hostname, pbar, index, output):
    logging.debug("Connecting to %s", hostname)

    try:

        pbar.update(1)
        cert = ssl.get_server_certificate((hostname, 443))  # Remove hardcoded port
        logging.debug("Got cert!")
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

        # output[index] += "Subject: " + str(x509.get_subject().CN)

        ext_count = x509.get_extension_count()

        if ext_count > 0:
            for i in xrange(ext_count):
                if "DNS:" in str(x509.get_extension(i)):
                    sans = str(x509.get_extension(i)).replace("DNS:", "").split(",")
                    sans_len = len(sans)
                    # output[index] += " Altnames: "

                    for i in xrange(sans_len):
                        if (sans_len > 1) & (i != sans_len - 1):
                            logging.debug("%s, ", str(sans[i]))
                            # output[index] += "%s, " % str(sans[i][1])
                            output[index] += "%s," % str(sans[i])
                        else:
                            logging.debug("%s", str(sans[i]))
                            output[index] += "%s" % str(sans[i])

    except socket.error:
        output[index] = "Connection refused - SSL not available or it isn't working."
        logging.debug("Connection refused - SSL not available or it isn't working.")

    except ssl.CertificateError as err:
        logging.debug(err)
        output[index] = "Connection refused - SSL not available or it isn't working."

    except Exception as err:
        logging.debug(err)
        output[index] = "Connection refused - SSL not available or it isn't working."


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
