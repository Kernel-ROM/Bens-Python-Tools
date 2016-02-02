# Python 2.7
import json, sys, array

# This sets up the key 'byte' array as permutation of the numbers 0-255
def keysetup(keyarray):
	keyarray = convert(keyarray)
	K = []
	for i in range(0, 256):
		K.append(i)
	j = 0
	for i in range(0,255):
		j = (j + K[i] + keyarray[i%len(keyarray)]) % 256
		K[i], K[j] = K[j], K[i]
	return K

def openfile(name):
	with open (name, "r") as file:
		return file.read().replace('\n', '')

# Converts an array of chars to unicode
def convert(string):
	return [ord(c) for c in string]

# Converts an array of unicode ints to a readable string
def chrconvert(string):
	return array.array('B', string).tostring()

# This turns the permutation from the keysetup func to an infinate 'byte' stream
def bytegen(K):
	i = 0
	j = 0
	while 1:
		i = (i + 1) % 256
		j = (j + K[i]) % 256
		K[i], K[j] = K[j], K[i]
		# allows for infinite values to be used without having to be pre-computed
		yield K[(K[i] + K[j]) % 256]

def encrypt(keyfile, text, output):
	plaintext = openfile(text)
	key = openfile(keyfile)
	PT = convert(plaintext)
	Keys = keysetup(key)
	Keygen = bytegen(Keys)
	encryptedstring =[]
	for i in range(0, len(PT)):
		xor = Keygen.next() ^ PT[i]
		# This 'hack' Converts the value to hex (without '0x'), forces upper case and ensures consistency of zeros
		xor = hex(xor)[2:].upper().zfill(2)
		encryptedstring.append(xor)
	with open(output, 'w') as outfile:
		json.dump(encryptedstring, outfile)
	#print ''.join(encryptedstring) # Outputs ciphertext the way the CW spec example does
	return

def decrypt(keyfile, text, output):
	key = openfile(keyfile)
	with open (output, "r") as textfile:
		encryptedtext = json.load(textfile)
	Keys = keysetup(key)
	Keygen = bytegen(Keys)
	plaintext = []
	for i in range(0, len(encryptedtext)):
		xor = Keygen.next() ^ int(encryptedtext[i], 16)
		plaintext.append(xor)
	decryptedstring = chrconvert(plaintext)
	print decryptedstring
	with open(text, 'w') as outfile:
		outfile.write(decryptedstring)
	return

def main(args):
	if len(sys.argv) != 5:
		print "Missing argument, you only supplied %d." % (len(sys.argv)-1)
		return
	if sys.argv[1] == "e":
		encrypt(sys.argv[2], sys.argv[3], sys.argv[4])
	elif sys.argv[1] == "d":
		decrypt(sys.argv[2], sys.argv[3], sys.argv[4])
	else:
		print "Incorrect argument(s) supplied."
		return

if __name__ == "__main__":
    main(sys.argv[1:])