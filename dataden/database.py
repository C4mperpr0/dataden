from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dataden.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    mail = db.Column(db.String(1), unique=True, nullable=False)
    username = db.Column(db.String(1), unique=True, nullable=False)
    password = db.Column(db.String(0), nullable=False)
    hash_salt = db.Column(db.String(0), nullable=False)
    settings = db.Column(db.String(0), nullable=False)
    design = db.Column(db.String(0), nullable=False)
    phone = db.Column(db.String(0), nullable=False)
    account_creation = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<User %r>' % self.username

class Verification(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    mail = db.Column(db.String(1), unique=True, nullable=False)
    username = db.Column(db.String(1), unique=True, nullable=False)
    password = db.Column(db.String(0), nullable=False)
    hash_salt = db.Column(db.String(0), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
