from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['secret_key'] = 'cum'
socketio = SocketIO(app)



from database import db

# class RandomBullshit(db.Model):
#     __tablename__ = 'random_bullshit'
#     stuff = db.Column(db.String(), primary_key=True)

if __name__ == '__main__':
    socketio.run(app)
    
