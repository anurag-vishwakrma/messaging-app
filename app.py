from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://message:message@localhost:5432/message_db'
db = SQLAlchemy(app)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)


@app.route('/')
def hello_world():
    with app.app_context():
        # Inside the context, you can perform database operations
        db.create_all()
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True,port=9000)
