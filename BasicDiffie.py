import random

def diffie():
	print "\n***************\n* Setup Stage *\n***************\n"
	# compute list of primes below a certain number
	primes = Primes(1000)
	
	# Choose random prime p
	p = primes[random.randrange(len(primes)-1)]
	primes.remove(p)
	# Choose Alice random private key
	privA = primes[random.randrange(len(primes)-1)]
	primes.remove(privA)
	# Choose Bob random private key
	privB = primes[random.randrange(len(primes)-1)]
	# Ensure g is a primitive root (use 2 or 5 normally)
	g = random.randrange(2, 6, 3)
	print "Step 1: p=%d & g=%d, privA=%d & privB=%d" % (p,g, privA, privB)

	# Compute for both keys (g exponent Private Key) mod p 
	gAmodp = g ** privA % p
	gBmodp = g ** privB % p

	print "\nStep 2: gAmodp=%d & gBmodp=%d" % (gAmodp, gBmodp)

	# Compute shared key by mixing other parties private exponent
	AKey = gAmodp ** privB % p
	BKey = gBmodp ** privA % p

	print "\nStep 3: Alice Key=%d & Bob Key=%d" % (AKey, BKey)

	# DHKE has been successful if both session keys are identical
	if AKey == BKey:
		print "\n*****************\n* DHK Complete! *\n*****************"
		print "\nSuccess! Alice & Bob have the same session key!"
	else:
		print "Something went wrong somewhere..."

	return

def Primes(n):
	# return list of primes < n
	sieve = [True] * n
	for i in xrange(3,int(n**0.5)+1,2):
		if sieve[i]:
			sieve[i*i::2*i]=[False]*((n-i*i-1)/(2*i)+1)
	return [2] + [i for i in xrange(3,n,2) if sieve[i]]

diffie()