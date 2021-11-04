import string
import hashlib
import random


def random_string(length):
    return ''.join(random.choices(string.digits + string.ascii_uppercase, k=length))  # some functions are not case sensitive


def stringcontents(checkString, checkFor=[string.digits, string.ascii_letters]):
    charList = ''.join(checkFor)
    return not any([(c not in charList) for c in list(checkString)])


def generate_salt(length=16):
    sys_random = random.SystemRandom()
    salt = list()
    for x in range(length):
        salt.append(sys_random.randint(0, 255))
    return bytes(salt)


def hashData(data, salt=b"1", inBytes=False):
    if inBytes:
        return hashlib.sha512(data.encode("utf8") + salt).digest()
    else:
        return hashlib.sha512(data.encode("utf8") + salt).hexdigest()
