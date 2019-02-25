import sys
import os.path
import tldextract

if (len(sys.argv) == 1) or (len(sys.argv) > 2):
    print("""Usage Examples:\t
        python root_domain_extract.py input_domains.txt > output_file.txt""")
    sys.exit(1)

if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1]) as f:
        domains = f.readlines()
    domains = [x.strip() for x in domains]  # Strip whitespace and newline chars
    domains_len = len(domains)

    for i in domains:
        print tldextract.extract(i).domain + "." + tldextract.extract(i).suffix

else:
    print("Incorrect argument(s), exiting.")
    sys.exit(1)
