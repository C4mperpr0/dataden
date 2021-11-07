import sqlclient
import tasklib

sqlclient.init(("127.0.0.1", 2110), b"1234")

def sql(query, values=tuple(), singleReturn=False):
    if not isinstance(values, tuple):
        values = (values, )
    r = sqlclient.request(query, values)
    if singleReturn:
        while isinstance(r, (list, tuple)) and len(r) == 1:
            r = r[0]
    print("-------------------------- SQL --------------------------")
    print(query)
    print(values)
    print(r)
    print("---------------------------------------------------------")
    return r


def new_user_id():
    while True:
        verification_id = tasklib.random_string(20)
        if sql(f'SELECT EXISTS(SELECT 1 FROM userdata WHERE user_id=? LIMIT 1)', verification_id, 1) or sql(
                f'SELECT EXISTS(SELECT 1 FROM verification WHERE verification_id=? LIMIT 1)', verification_id, 1):
            continue
        return verification_id


def new_chat_id():
    while True:
        chat_id = tasklib.random_string(20)
        if sql(f'SELECT EXISTS(SELECT 1 FROM chats WHERE chat_id=? LIMIT 1)', chat_id, 1):
            continue
        return chat_id


def check_login(mail, password, table='userdata', verification_key=None, verification_id=None):
    if sql(f'SELECT EXISTS(SELECT 1 FROM {table} WHERE mail=? LIMIT 1)', (mail.lower()), 1):
        user_data = to_json(sql(f'SELECT * FROM {table} WHERE mail=?', (mail.lower())), table)
        if verification_key is not None:
            verification_id_match = verification_id == user_data[verification_key]
        else:
            verification_id_match = True  # no key need because its regular login, not verification
        r = user_data if (user_data['password'] == tasklib.hashData(
            password, user_data["hash_salt"]) and verification_id_match) else None  # !!!!! Fix: don't forget to insert salt here
    else:
        r = None
    if r is not None and verification_key is not None:  # verification_key != None means that it's an verification, not an login
        sql(f'INSERT INTO userdata (mail, username, user_id, password, hash_salt, design, mail_visible, phone_visible) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (mail.lower(), user_data["username"], verification_id, user_data["password"], user_data["hash_salt"], "default", 1, 1))
        sql(f'DELETE FROM verification WHERE verification_id=?', verification_id)
    return r


"""
    def add_user(self, user_data, auto_conn=True):
        if auto_conn:
            self.connect()
        new_user_data = {'mail': user_data['mail'],
                         'username': user_data['username'],
                         'user_id': user_data['verification_id'],
                         'password': user_data['password'],
                         'settings': None,
                         'design': 'default',
                         'phone': None,
                         'mail_visible': True,
                         'phone_visible': True}
        cursor = self.conn.cursor()
        cursor.execute(
            f'INSERT INTO userdata ({", ".join(new_user_data.keys())}) VALUES ({", ".join(? * len(new_user_data.values()))})',
            tuple(new_user_data.values()))
        self.conn.commit()
        if auto_conn:
            self.disconnect()
            

    def del_row_by_id(self, table, key, value, auto_conn=True):
        if auto_conn:
            self.connect()
        cursor = self.conn.cursor()
        cursor.execute(f'DELETE FROM {table} WHERE {key}="{value}"')
        self.conn.commit()
        if auto_conn:
            self.disconnect()


def getChatMessageChunks(chat_id, index=-1):
    if index == -1:
        index = self.custom_select(
    chunks = [((index - 50) if (index - 50) >= 0 else 0), index]
    messages = self.custom_select(f'SELECT message_id, user_id, message, time, content FROM messages WHERE chat_id=\"{chat_id}\" AND message_id BETWEEN {chunks[0]} AND {chunks[1]}', auto_conn=False)
    return messages
"""


def to_json(data, table, force_list=False):
    if table == 'userdata':
        r = {'mail': [d[0] for d in data],
             'username': [d[1] for d in data],
             'user_id': [d[2] for d in data],
             'password': [d[3] for d in data],
             'hash_salt': [d[4] for d in data],
             'settings': [d[5] for d in data],
             'design': [d[6] for d in data],
             'phone': [d[7] for d in data],
             'mail_visible': [d[8] for d in data],
             'phone_visible': [d[9] for d in data],
             'account_creation': [d[10] for d in data]}
    elif table == 'verification':
        r = {'mail': [d[0] for d in data],
             'username': [d[1] for d in data],
             'password': [d[2] for d in data],
             'hash_salt': [d[3] for d in data],
             'verification_id': [d[4] for d in data],
             'next_request': [d[5] for d in data]}
    elif table == 'chats':
        r = {'chat_id': [d[0] for d in data],
             'members_id': [d[1] for d in data],
             'members_name': [d[2] for d in data],
             'type': [d[3] for d in data],
             'picture': [d[4] for d in data]}
    elif table == 'messages':
        r = {'chat_id': [d[0] for d in data],
             'message_id': [d[1] for d in data],
             'username': [d[2] for d in data],
             'message': [d[3] for d in data],
             'time': [d[4] for d in data],
             'content': [d[5] for d in data]}
    else:
        r = {}
    if not force_list:
        for k in r.keys():
            if (len(r[k]) == 1):
                r[k] = r[k][0]
            elif (len(r[k]) == 0):
                r[k] = None
    return r


def setupDB():
    sql('''CREATE TABLE userdata (
                    mail TEXT,
                    username TEXT,
                    user_id TEXT,
                    password TEXT,
                    hash_salt BLOB,
                    settings TEXT,
                    design TEXT,
                    phone TEXT,
                    mail_visible TEXT,
                    phone_visible TEXT,
                    account_creation DATETIME,
                    PRIMARY KEY("user_id")
                    )''')
    sql('''CREATE TABLE verification (
                    mail TEXT,
                    username TEXT,
                    password TEXT,
                    hash_salt BLOB,
                    verification_id TEXT,
                    next_request DATETIME,
                    PRIMARY KEY("verification_id")
                    )''')
    sql('''CREATE TABLE chats (
                    chat_id TEXT,
                    members_id TEXT,
                    members_name TEXT,
                    type TEXT,
                    picture TEXT,
                    PRIMARY KEY("chat_id")
                    )''')
    # type -> dm, group, broadcast
    sql('''CREATE TABLE messages (
                    chat_id TEXT,
                    message_id TEXT,
                    user_id TEXT,
                    message TEXT,
                    time DATETIME,
                    content TEXT,
                    PRIMARY KEY("message_id")
                    )''')
    sql('''CREATE TABLE filestorage (
                        file_id TEXT,
                        file_path TEXT,
                        storage TEXT,
                        type TEXT,
                        file_name TEXT,
                        creation_time DATETIME,
                        file_size INT,
                        PRIMARY KEY("file_id")
                        )''')
    # storage -> webdrive, projectdrive, ...
    # type -> file, directory
    sql('''CREATE TABLE remotecontrol (
                        device_id TEXT,
                        os TEXT,
                        owner TEXT,
                        co_users TEXT
                        device_name,
                        veify_expiry DATETIME,
                        info TEXT,
                        PRIMARY KEY("device_id")
                        )''')
