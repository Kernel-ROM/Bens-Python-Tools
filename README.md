# Ben's Naughty Python Tools
A collection of useful or malicious python scripts created for educational purposes.

These are perfect for deployment on a targets system as a lot of A/V products will white-list python applications. Coupled with a freezing utility like [py2exe](http://www.py2exe.org/) or [pyinstaller](http://www.pyinstaller.org/), these can be executed on any Windows machine regardless of whether python is installed or not!

## Pycurious

This tool is essentially an undetected reverse shell written using the Python socket module.

- Phase One: Start a netcat listening server the usual way.
- Phase Two: Get the target user to launch pycurious.
- Phase Three: ???
- Phase Four: **Profit!**

## isPy

This is a very small, yet highly flexible python keylogger (WIP)