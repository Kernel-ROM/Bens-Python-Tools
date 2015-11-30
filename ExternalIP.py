import requests, sys

try:
	response = requests.get("https://api.ipify.org/?format=json")
except:
	print "Connection failed."
	sys.exit(1)
ip = response.json()
print "\nYour external IP adress is: %s\n" % ip['ip']
