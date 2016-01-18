import random
from fractions import gcd

def Demo():
	print "\n***************\n* Setup Stage *\n***************\n"
	# compute list of primes below a certain number
	primes = Primes(1000)

	# choose two randomly, ensuring they're different
	p = primes[random.randrange(len(primes)-1)]
	primes.remove(p)
	q = primes[random.randrange(len(primes)-1)]

	print "Step 1: p=%d & q=%d" % (p,q)
	# Determine the product(n) of p & q
	ProductOfPrime = p*q
	print "\nStep 2: p*q = %d" % ProductOfPrime

	#Due to q&q being prime, totient is prime-1
	totient = (p-1) * (q-1)
	print "\nStep 3: Totient = %d" % totient

	plist = []
	# Determine which numbers in range have only one common divisor
	for i in range(2, totient+1):
		# gcd = Greatest Common Divisor
		if (gcd(i, totient) == 1):
			plist.append(i)
	# print plist
	# Public(e) is then chosen randomly from list of ints
	PublicKey = plist[random.randrange(len(plist)-1)]
	print "\nStep 4: Random Public Key = %d" % PublicKey

	# Ensure private(d) is larger than p or q
	# so start i from the largerof the two
	if p > q:
		i = p
	else:
		i = q
	while 1:
		# compute private(d) so that d*e = 1 mod totient 
		if (PublicKey * i) % totient == 1:
			break
		else:
			i = i+1
	PrivateKey = i
	print "\nStep 5: Private Key = %d\n" % PrivateKey

	print "*************************\n* Encrypt/Decrypt Stage *\n*************************"
	ciphertext = Encrypt(plaintext, PublicKey, ProductOfPrime)
	decryptext = Decrypt(ciphertext, PrivateKey, ProductOfPrime)

	print "\nPlaintext is: %d" % plaintext
	print "\nEncrypted text is: %d" % ciphertext
	print "\nDecrypted text is: %d" % decryptext
	return

def Encrypt(plaintext, publicKey, PoP):
	return(plaintext**publicKey % PoP)

def Decrypt(ciphertext, privateKey, PoP):
	return(ciphertext**privateKey % PoP)

def Primes(n):
	# return list of primes < n
	sieve = [True] * n
	for i in xrange(3,int(n**0.5)+1,2):
		if sieve[i]:
			sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
	return [2] + [i for i in xrange(3,n,2) if sieve[i]]

# Choose random plaintext int 1-99
plaintext = random.randrange(1,999)
Demo()