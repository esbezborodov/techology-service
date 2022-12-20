from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_login import UserMixin
import os


app=Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)


class Products(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    type=db.Column(db.String(100))
    name=db.Column(db.String(100))
    description=db.Column(db.Text)
    manufacturer=db.Column(db.String(100))
    price=db.Column(db.Integer)
    photo=db.Column(db.String(500))


class Users(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    login=db.Column(db.String(50), unique=True, nullable=False)
    password=db.Column(db.String(100), nullable=False)
    admin=db.Column(db.Boolean, default=False)


class Comments(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    prod_id=db.Column(db.Integer)
    like=db.Column(db.Integer)
    comment=db.Column(db.Text)


with app.app_context():
    db.create_all()