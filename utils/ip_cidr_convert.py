from netaddr import cidr_merge, iter_iprange, IPNetwork
import sys

if (len(sys.argv) == 1) or (len(sys.argv) > 2):
    print("""Usage Examples:\t
        python ip_cidr_convert 192.168.1.0-192.168.1.255
        python ip_cidr_convert 192.168.1.0/24""")
    sys.exit(1)

if "-" in sys.argv[1]:
    r = sys.argv[1].split("-")
    ip_r = list(iter_iprange(r[0], r[1]))
    ip_r_list = cidr_merge(ip_r)
    for ip_range in ip_r_list:
        print ip_range

elif "/" in sys.argv[1]:
    r = IPNetwork(sys.argv[1])
    print "%s - %s" % (r[0], r[len(r) - 1])

else:
    print("Incorrect argument(s), exiting.")
    sys.exit(1)
