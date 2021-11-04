import socket
import hashlib
import pickle

# Please read the documentation before using.

addr = None
password = None

def init(addr_: tuple, password_: bytes):
    global addr, password
    addr = addr_
    password = password_

def verify_request(request):
    global password

    # Verification hash is SHA-1, length 20
    verification = request[-20:]
    raw_request = request[:-20]

    return hashlib.sha1(raw_request + password).digest() == verification

def request(reqstr: str, args: tuple):
    global addr, password
    
    # See docs/protocol

    req = pickle.dumps((reqstr, args))
    verification = hashlib.sha1(req + password).digest()

    full = req + verification

    content_length = len(full)

    content_length = content_length.to_bytes(4, byteorder="little", signed=False)

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.settimeout(20.0)
    c.connect(addr)

    c.sendall(content_length)
    c.sendall(full)

    content_length = int.from_bytes(c.recv(4), byteorder="little", signed=False)
    answer = c.recv(content_length)

    c.close()

    if not verify_request(answer):
        return False

    answer = answer[:-20]

    return pickle.loads(answer)