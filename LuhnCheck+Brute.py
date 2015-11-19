import itertools, sys

def luhnbool(cc):
	return (sum(cc[0::2]) + sum(sum(divmod(d*2,10)) for d in cc[1::2])) % 10 == 0

def bruteforce(length):
	charset = '0123456789'
	return (''.join(candidate)
		for candidate in itertools.chain.from_iterable(itertools.product(charset, repeat=i)
		for i in range(length, length + 1)))

def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

def main():
	missing = False
	if len(sys.argv) > 1:
		cc = sys.argv[1]
		print "Validating: %s" % cc
	else:
		cc = raw_input("Number to check: ")
	if len(cc) % 2 != 0:
		print "Invalid number (should be even)"
		return

	ccl = list(cc)
	ccl = list(reversed(ccl))
	for i in range(len(ccl)):
		if ccl[i] == "?":
			missing = True
			pass
		else:
			ccl[i] = int(ccl[i])

	if missing == False:
		if luhnbool(ccl) == True:
			print "Number passed Luhn check."
		elif luhnbool(ccl) == False:
			print "Number failed Luhn check."
		else:
			print "Exception occured!"
	elif missing == True:
		missingno = list_duplicates_of(ccl, "?")
		missingnoprint = [len(ccl)-x for x in missingno]
		print "Detected missing number(s) at position(s) " + ', '.join(map(str, missingnoprint))
		brute = list(bruteforce(len(missingno)))
		print "\nPotential digits: "
		for i in range(len(brute)):
			split = [int(k) for k in str(brute[i])]
			for j in range(len(missingno)):
				ccl[missingno[j]] = split[j]
			if luhnbool(ccl) == True:
				print "  " + brute[i][::-1]
if __name__ == "__main__":
    main()