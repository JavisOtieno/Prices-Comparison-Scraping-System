from app import app
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import request
import socket

# Get the current machine's hostname
hostname = socket.gethostname()
print("hostname",hostname,hostname == 'DESKTOP-6FGNSTO')

if hostname == 'DESKTOP-6FGNSTO' or hostname == 'your-local-machine-name':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/avke'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Billion%4023@localhost/avkenew'


current_path = os.getcwd()  # Or use __file__ if checking within a specific file
# Check if '/var/' is in the path
# Removed var check in current path as getcwd producing / as the result
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/avke'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Billion%4023@localhost/avkenew'


# @app.route('/viewdbstatus')
# def viewdbstatus():
#     return app.config['SQLALCHEMY_DATABASE_URI']+" -- Path:"+current_path


db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    commission = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    image = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    highlights = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    cart_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    websitename = db.Column(db.Text, nullable=False)
    websitevisits = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Text, nullable=False)
    total = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)



class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.title}>'
