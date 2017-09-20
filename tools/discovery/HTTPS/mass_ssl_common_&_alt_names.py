#!/usr/bin/env python
"""
Quick tool to mass pull the Common Name and Subject Alt Names from SSL certs. Requires: tqdm & dnspython
TODO: Threading
"""
import ssl
import sys
import socket
import argparse
import logging
from tqdm import tqdm

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--infile", help="input file", required=True)
    parser.add_argument("-o", "--outfile", help="output file", required=True)
    # parser.add_argument("-T", "--threads", help="number of threads to run, default is 10",
    #                    nargs="?", const=1, type=int, default=10)
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

    print "Preparing to analyse %s certs\n\n" % str(len(domains))

    for hostname in tqdm(domains, disable=bar_disable):

        logging.debug("Connecting to %s", hostname)

        try:
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(socket.socket(), server_hostname=hostname)
            s.connect((hostname, 443))
            cert = s.getpeercert()

            subject = dict(x[0] for x in cert['subject'])
            issued_to = subject['commonName']

            logging.debug("Issued to: %s", issued_to)

            out_file.write("Issued to: " + str(issued_to))

            try:
                alt_names = cert['subjectAltName']
                out_file.write(" - Alt Names: ")

                for i in xrange(len(alt_names)):
                    if (len(alt_names) > 1) & (i != len(alt_names) - 1):
                        logging.debug("%s, ", str(alt_names[i]))
                        out_file.write("%s, " % str(alt_names[i][1]))
                    else:
                        logging.debug("%s ", str(alt_names[i]))
                        out_file.write("%s " % str(alt_names[i][1]))

            except AttributeError:
                logging.debug("Hit attribute error!")
                continue

        except socket.error:
            logging.debug("Connection error!")
            out_file.write("Connection refused - SSL not available or it isn't working.")
            continue

        except ssl.CertificateError as err:
            logging.debug(err)
            out_file.write(err)
            continue

        out_file.write("\n")

    print "\nFinished!"


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print "\nExiting..."
        pass
