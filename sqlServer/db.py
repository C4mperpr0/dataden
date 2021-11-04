import sqlite3
import multiprocessing
import traceback

def check_queue(pipe_queue, DATABASE):
    # Should be called as a separate proc
    db = sqlite3.connect(DATABASE)
    while True:
        pipe = pipe_queue.get()
        try:
            # i hope this is self-explanatory enough
            request = pipe.recv()

            assert type(request[0]) == str
            assert type(request[1]) == tuple
            
            cursor = db.cursor()
            cursor.execute(request[0], request[1])
            db.commit()
            ans = cursor.fetchall()
        except Exception as exc:
            ans = (exc, traceback.format_exc())
        finally:
            pipe.send(ans)
            pipe.close()