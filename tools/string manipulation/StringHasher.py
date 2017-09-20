"""Hash a given string using the six most common algorithms."""
import hashlib
import string

# print hashlib algorithms
hash_list = "MD5\nSHA1\nSHA224\nSHA256\nSHA384\nSHA512\n"
print hash_list
print "Please choose a hash function: "
hash_choice = raw_input()
print "\nEnter a string to hash: "
my_string = raw_input()

if hash_choice.upper() == "MD5":
    print("\n" + hashlib.md5(my_string).hexdigest())
elif hash_choice.upper() == "SHA1":
    print("\n" + hashlib.sha1(my_string).hexdigest())
elif hash_choice.upper() == "SHA224":
    print("\n" + hashlib.sha224(my_string).hexdigest())
elif hash_choice.upper() == "SHA256":
    print("\n" + hashlib.sha256(my_string).hexdigest())
elif hash_choice.upper() == "SHA384":
    print("\n" + hashlib.sha384(my_string).hexdigest())
elif hash_choice.upper() == "SHA512":
    print("\n" + hashlib.sha512(my_string).hexdigest())
else:
    print("\nUnlisted algorithm, Exiting...")
