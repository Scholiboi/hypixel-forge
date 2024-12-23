from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    amount = db.Column(db.Integer, unique=False, nullable=False)
