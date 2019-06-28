val=8 #Provide the Length for the Password
option='2' # provide option for selecting the operation to perform
#option 1: Generating Random Password using Upper Case
#option 2: Generating Random Password using Lower Case
#option 3: Generating Random Password using Upper Case, Lower case and Special Characters
#option 4: Generating Random Password using Upper Case and Special Characters
#option 5: Generating Random Password using Lower Case and Special Characters
import string
import random

def pw_gen_spl(size, chars=string.ascii_uppercase + string.digits + string.punctuation + string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size))

def pw_gen_ucase(size, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

def pw_gen_lcase(size, chars=string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def pw_gen_lcase_spl(size, chars=string.ascii_lowercase + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))

def pw_gen_ucase_spl(size, chars=string.ascii_uppercase + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))

if option == '1':
    print "Random generated Password with Upper Case"
    print (pw_gen_ucase(val, chars=string.ascii_uppercase ))

if option == '2':
    print "Random  generated Password with Lower Case"
    print (pw_gen_lcase(val, chars=string.ascii_lowercase))

if option == '3':
    print "Random generated Password with special characters, upper and lower case string"
    print (pw_gen_spl(val, chars=string.ascii_uppercase + string.digits + string.punctuation + string.ascii_letters))

if option == '4':
    print "Random generated password with Upper Case and Special Characters"
    print (pw_gen_lcase_spl(val, chars=string.ascii_lowercase + string.punctuation))

if option == '5':
    print "Random generated Password with Lower Case and Special Characters"
    print (pw_gen_lcase_spl(val, chars=string.ascii_uppercase + string.punctuation))

if not option:
    print "No such option"
