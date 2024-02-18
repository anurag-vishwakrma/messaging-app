from extension import db
from sqlalchemy import DateTime, func


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    reply_msg_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    text = db.Column(db.String(512))
    msg_date = db.Column(DateTime(timezone=True), server_default=func.now())
    chat_user_id = db.Column(db.Integer)
