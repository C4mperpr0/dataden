import os
import json
import base64


class Serverconfig:
    def __init__(self):
        standard = {'session_secret_key': os.urandom(24),
                    'server_mail': {'user': '', 'password': '', 'address': 'smtp.gmail.com', 'port': 587},
                    'server_ip': '127.0.0.1',
                    'server_port': 8080,
                    'debug': True,
                    'threading': True,
                    'fileuploadpath': r"/uploads"
                    }
        if 'serverconfig.json' in os.listdir('./'):
            with open('./serverconfig.json', 'rb') as file:
                conf = json.loads(file.read().decode('utf-8'))
                if 'session_secret_key' in conf.keys():
                    conf['session_secret_key'] = base64.b64decode(conf['session_secret_key'].encode('ascii'))
                for attr in standard.keys():
                    if attr not in conf.keys():
                        conf[attr] = standard[attr]
        else:
            conf = standard
        self.config = conf
        self.save()

    def set_config(self, attr, value):
        self.config[attr] = value
        self.save()

    def get(self, attr):
        return self.config[attr]

    def save(self):
        with open('./serverconfig.json', 'wb') as file:
            conf = self.config
            conf['session_secret_key'] = base64.b64encode(conf['session_secret_key']).decode('ascii')
            file.write(json.dumps(conf, indent=4).encode('utf-8'))

    def new_session_secret(self):
        self.config['session_secret_key'] = os.urandom(24)
        self.save()
