# Ben's Python Tools
A collection of useful or malicious python scripts created for educational purposes.

These are perfect for deployment on a targets system as a lot of A/V products will white-list python applications. Coupled with a freezing utility like [py2exe](http://www.py2exe.org/) or [pyinstaller](http://www.pyinstaller.org/), these can be executed on any Windows machine regardless of whether python is installed or not!


## Pycurious

This tool is essentially an undetected reverse shell written using the Python socket module.

- Phase One: Start a netcat listening server the usual way.
- Phase Two: Get the target user to launch pycurious.
- Phase Three: ???
- Phase Four: **Profit!**

Custom Commands:
	qqq - Close connection
	winstart! - Moves itself to the windows startup folder for persistence
	FUBAR! - Closes the connection and deletes itself in case of detection


## Luhn Checker + Bruteforcer

This program allows you to check if a given number passes the Luhn algorithm test. This is the algorithm used extensively by banks and websites to verify credit and debit cards, however this is kind of <b>boring!</b>

The <b>exciting</b> feature is that if you replace any digit with a question mark, it will brute-force the values until it finds combinations of integers that satisfy the Luhn algorithm.

<b>Pro tip: Don't post pictures of your credit card on the internet, thinking you're safe because you covered the last digits with your finger...</b>


## ExternalIP

Does what it says on the tin, queries an external API to determine your external IP address

## isPy

This is a very small, highly flexible python keylogger with options to either record the keystrokes locally or email them back to the atacker...(WIP)


## String Hasher

This is a quick and dirty script put together to allow you to hash any string via many different algorithms.


## Basic RSA

This is a very basic implementation of the RSA algorithm, for educational purposes only!


## Basic Diffie

This is a very basic implementation of the Diffie Hellman Key Exchange algorithm, for educational purposes only!