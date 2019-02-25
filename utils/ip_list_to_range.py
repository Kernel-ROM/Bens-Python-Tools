import ipaddress
import os
import sys
import netaddr

# python3 ip_list_to_range.py infile > outfile

if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as f:
        ips = f.readlines()
    ips = [x.strip() for x in ips]  # Strip whitespace and newline chars
    ips_len = len(ips)

nets = [ipaddress.ip_network(_ip) for _ip in ips]
cidrs = list(ipaddress.collapse_addresses(nets))

blocks = []

for c in cidrs:
    blocks.append(netaddr.IPNetwork(str(c)))

nets = netaddr.IPSet(blocks)

for cidr in nets.iter_cidrs():
    print(cidr)
