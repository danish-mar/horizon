# app/models.py

# from datetime import datetime
# from .db import db  # Import SQLAlchemy instance
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(128))
#     accounts = db.relationship('Account', backref='owner', lazy=True)
#
# class Account(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     account_number = db.Column(db.String(20), unique=True, nullable=False)
#     account_type = db.Column(db.String(20), nullable=False)
#     balance = db.Column(db.Float, default=0.0)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     transactions = db.relationship('Transaction', foreign_keys='Transaction.account_id', backref='account', lazy=True, cascade="all, delete-orphan")
#
# class Transaction(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
#     amount = db.Column(db.Float, nullable=False)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     transaction_type = db.Column(db.String(20), nullable=False)
#     description = db.Column(db.String(255))
#     related_account_id = db.Column(db.Integer, nullable=True)
#
#     def __repr__(self):
#         return f'<Transaction {self.id} - {self.transaction_type} - {self.amount}>'
