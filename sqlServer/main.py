import socket
import multiprocessing
import logging
import traceback
import sqlite3

import db
import clhandler
import mtlogger
import config

# Please read the documentation before using.

CONFIG = "config.json"

if __name__ == "__main__":
    # Read the config
    cfg = config.Config(CONFIG).config

    clhandler.set_password(cfg["shared_password"].encode("utf8"))

    # Create the multithreaded logger
    logger_queue = multiprocessing.Queue()
    logger = mtlogger.MultithreadedLogger(logger_queue, cfg["logging_level"])
    logger_proc = multiprocessing.Process(target=logger.logging_mainloop)
    logger_proc.start()

    # Create the process that does the database handling
    db_pipe_queue = multiprocessing.Queue()
    db_proc = multiprocessing.Process(target=db.check_queue, args=(db_pipe_queue, cfg["database"]))
    db_proc.start()

    # Create Server socket and bind it to all addresses and port
    # consider upgrading this to support ipv6 in the future if it doesn't already
    # (too lazy to look it up right now, but i think just changing it to socket.AF_INET6 might work)
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind(("", cfg["server_port"]))
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.settimeout(5.0)
    serv.listen(10)

    logger.log("info", "Server bound to all addresses on port " + str(cfg["server_port"]))

    while True:
        try:
            # On client connect -> Create pipe between it and db thread, start process to
            # handle connection
            client, addr = serv.accept()
            cl_pipe, db_pipe = multiprocessing.Pipe()
            db_pipe_queue.put(db_pipe)
            proc = multiprocessing.Process(target=clhandler.handle_client, args=(client, addr, cl_pipe, logger))
            proc.start()
        except socket.timeout:
            logger.log("debug", "serv.accept timed out")
        except Exception as exc:
            logger.log("error", traceback.format_exception(None, exc, exc.__traceback__))
