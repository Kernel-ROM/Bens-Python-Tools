from netaddr import IPNetwork, cidr_merge, iter_iprange
import sys
import os.path

if (len(sys.argv) == 1) or (len(sys.argv) > 2):
    print("""Usage Examples:\n\tpython ip_range_to_list.py 192.168.1.0/24 > output_file.txt
        python ip_range_to_list 192.168.1.0-192.168.1.255 > output_file.txt
        python ip_range_to_list input_range_file.txt > output_file.txt""")
    sys.exit(1)


if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as f:
        ranges = f.readlines()
    ranges = [x.strip() for x in ranges]  # Strip whitespace and newline chars
    range_len = len(ranges)

    for i in ranges:
        if "/" in i:
            for ip in IPNetwork(i):
                print ip
        elif "-" in i:
            r = i.split("-")
            ip_r = list(iter_iprange(r[0], r[1]))
            ip_r_list = cidr_merge(ip_r)
            for ip_range in ip_r_list:
                for ip in IPNetwork(ip_range):
                    print ip

elif "/" in sys.argv[1]:
    for ip in IPNetwork(sys.argv[1]):
        print ip
elif "-" in sys.argv[1]:
    r = sys.argv[1].split("-")
    ip_r = list(iter_iprange(r[0], r[1]))
    ip_r_list = cidr_merge(ip_r)
    for ip_range in ip_r_list:
        for ip in IPNetwork(ip_range):
            print ip
else:
    print("Incorrect argument(s), exiting.")
    sys.exit(1)
