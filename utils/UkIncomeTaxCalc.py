import sys

if len(sys.argv) == 1:	
	print ("Please enter your annual wage")
	wge = int(raw_input("> \x9c"))
elif len(sys.argv) == 2:
	wge = int(sys.argv[1])
elif len(sys.argv) > 2:
	print ("Too many arguments, takes only one!")
	sys.exit(1)

if wge < 10601:
	TI = wge
elif wge < 42386:
	PA = wge - 10600
	TI = PA * 0.68
	TI += 10600
elif wge > 42385 and wge < 150000:
	PA = wge - 10600
	TI = PA * 0.58
	TI += 10600
elif wge > 150000:
	PA = wge - 10600
	TI = PA * 0.53
	TI += 10600

tax = wge - TI
month = float(TI) / 12
TI, tax, month = "{:,}".format(int(TI)), "{:,}".format(int(tax)), "{:,}".format(int(month))
print ("\nYour annual pay minus tax comes to \x9c%s...") % (TI)
print ("\tWhich is \x9c%s per month.\n") % (month)
print ("You will pay \x9c%s in tax.") % (tax)