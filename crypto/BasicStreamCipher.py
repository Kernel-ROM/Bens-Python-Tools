"""
Basic Python implementation of a steam cipher protocol.

Definitely insecure, use for educational purposes only.
"""
import json
import sys
import array


def keysetup(keyarray):
    """Set up the key 'byte' array as permutation of the numbers 0-255."""
    keyarray = convert(keyarray)
    finalkey = []
    for i in range(0, 256):
        finalkey.append(i)
    j = 0
    for i in range(0, 255):
        j = (j + finalkey[i] + keyarray[i % len(keyarray)]) % 256
        finalkey[i], finalkey[j] = finalkey[j], finalkey[i]
    return finalkey


def openfile(name):
    """Standard file function."""
    with open(name, "r") as file:
        return file.read().replace('\n', '')


def convert(string):
    """Convert an array of chars to unicode."""
    return [ord(c) for c in string]


def chrconvert(string):
    """Convert an array of unicode ints to a readable string."""
    return array.array('B', string).tostring()


def bytegen(k):
    """Turn the permutation from keysetup into an infinate byte stream."""
    i = 0
    j = 0
    while 1:
        i = (i + 1) % 256
        j = (j + k[i]) % 256
        k[i], k[j] = k[j], k[i]
        # allows for infinite values without having to be pre-compute
        yield k[(k[i] + k[j]) % 256]


def encrypt(keyfile, text, output):
    """Encrypt input string using key string."""
    plaintext = openfile(text)
    key = openfile(keyfile)
    pt = convert(plaintext)
    keys = keysetup(key)
    keygen = bytegen(keys)
    encryptedstring = []
    for i in range(0, len(pt)):
        xor = keygen.next() ^ pt[i]
        # Converts the value to hex (without '0x')
        # Alsoforces upper case and ensures consistency of zeros
        xor = hex(xor)[2:].upper().zfill(2)
        encryptedstring.append(xor)
    with open(output, 'w') as outfile:
        json.dump(encryptedstring, outfile)
    return


def decrypt(keyfile, text, output):
    """Decrypt input string using key string."""
    key = openfile(keyfile)
    with open(output, "r") as textfile:
        encryptedtext = json.load(textfile)
    keys = keysetup(key)
    keygen = bytegen(keys)
    plaintext = []
    for i in range(0, len(encryptedtext)):
        xor = keygen.next() ^ int(encryptedtext[i], 16)
        plaintext.append(xor)
    decryptedstring = chrconvert(plaintext)
    print decryptedstring
    with open(text, 'w') as outfile:
        outfile.write(decryptedstring)
    return


def main(args):
    if len(sys.argv) != 5:
        print "Missing argument, you only supplied %d." % (len(sys.argv) - 1)
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
