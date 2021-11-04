import socket
import multiprocessing
import logging
import traceback
import hashlib
import pickle
import os

import db

password = ""

def set_password(pw):
    global password
    password = b'1234'

def verify_request(request, logger):
    global password
    password = b'1234'

    # Verification hash is SHA-1, length 20
    verification = request[-20:]
    raw_request = request[:-20]

    logger.log("debug", verification)
    logger.log("debug", raw_request)
    print(verification)
    print(raw_request)

    return hashlib.sha1(raw_request + password).digest() == verification

def handle_client(client, addr, cl_pipe, logger):
    global password

    id = str(os.getpid())
    client.settimeout(20.0)

    try:
        # See docs/protocol for info
        logger.log("info", id + " Connection from " + addr[0] + ", waiting for CL")
        content_length = client.recv(4)
        content_length = int.from_bytes(content_length, byteorder="little", signed=False)

        logger.log("info", id + " CL="+str(content_length))
        request = client.recv(content_length)

        if not verify_request(request, logger):
            logger.log("warn", id + " Client verification failed")
            return False

        logger.log("info", id + " In DB queue...")

        cl_pipe.send(pickle.loads(request[:-20]))

        answer = cl_pipe.recv()
        answer = pickle.dumps(answer)

        verification = hashlib.sha1(answer + password).digest()
        answer = answer + verification
        content_length = len(answer).to_bytes(4, byteorder="little", signed=False)

        logger.log("info", id + " Sending answer, CL="+str(len(answer)))

        client.sendall(content_length)
        client.sendall(answer)

        logger.log("info", id + " Done")
    finally:
        client.close()
