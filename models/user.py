from extension import db
from sqlalchemy import DateTime, func


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))
    display_name = db.Column(db.String(180))
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(13), unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_super_user = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(DateTime(timezone=True), server_default=func.now())
