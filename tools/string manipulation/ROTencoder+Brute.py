import sys

# Common English stop words
words = ["the", "your", "to", "of", "and", "in", "that", "have", "i", "a", "puzzle",
	"it", "for", "not", "on", "with", "this", "he", "you", "do", "at", "is", "job"]

def encode(s, n):
	# Keep n below 26
	n = n % 26
	abc = "abcdefghijklmnopqrstuvwxyz" * 2
	abc = abc + abc.upper()
	def get_i():
		for i in range(26):
			yield i
		for i in range(53, 78):
			yield i
	ROT = {abc[i]: abc[i+n] for i in get_i()}
	return "".join(ROT.get(i,i) for i in s)

def decode(s, n):
	n = n % 26
	# Decode operation is same as encode - 26
	return encode(s, abs(n % 26 - 26))

def bruteROT(s):
	no = [0, 0]
	# Compare decoded statements
	def common(l1, l2):
		result = []
		for i in l1:
			if i.lower() in l2:
				result.append(i)
		return len(result)
	for i in range(1, 26):
		brute = decode(s, i)
		arr = brute.split()
		share = common(arr, words)
		if share > no[1]:
			no[0] = i
			no[1] = share
	if no[1] == 0:
		return "Error! Unknown encoding"
	else:
		s = decode(s, no[0])
		return "Decoded using ROT%d: \n %s" % (no[0], s)

def main():
	if len(sys.argv) < 3:
		print "Missing argument(s), you only supplied %d." % (len(sys.argv)-1)
		return
	if sys.argv[1] == "e":
		print encode(sys.argv[2], int(sys.argv[3]))
	elif sys.argv[1] == "d":
		print decode(sys.argv[2], int(sys.argv[3]))
	elif sys.argv[1] == "b":
		print bruteROT(sys.argv[2])
	else:
		print "Incorrect argument(s) supplied."
		return

if __name__ == "__main__":
    main()