from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://cum.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class RandomBullshit(db.Model):
    __tablename__ = 'random_bullshit'
    stuff = db.Column(db.String(), primary_key=True)