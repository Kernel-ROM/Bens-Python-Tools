from netaddr import IPAddress
import sys
import os.path

if (len(sys.argv) == 1) or (len(sys.argv) > 2):
    print("""Usage Examples:\t
        python subnetmask_cidr_convert.py input_mask_file.txt > output_file.txt""")
    sys.exit(1)

if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as f:
        ranges = f.readlines()
    ranges = [x.strip() for x in ranges]  # Strip whitespace and newline chars
    range_len = len(ranges)

    for i in ranges:
        print "/" + str(IPAddress(i).netmask_bits())

else:
    print("Incorrect argument(s), exiting.")
    sys.exit(1)
