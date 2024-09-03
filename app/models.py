from app import app
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy



current_path = os.getcwd()  # Or use __file__ if checking within a specific file
# Check if '/var/' is in the path
# Removed var check in current path as getcwd producing / as the result
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/avke'

@app.route('/viewdbstatus')
def viewdbstatus():
    return app.config['SQLALCHEMY_DATABASE_URI']+" -- Path:"+current_path


db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, nullable=True, onupdate=datetime.utcnow)

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Float, nullable=False)
    customer_id = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text, nullable=False)
    cart_id = db.Column(db.Float, nullable=False)
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
