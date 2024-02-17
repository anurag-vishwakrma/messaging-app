from flask import Flask
from flask_migrate import Migrate
from routes.auth import auth_bp
from extension import db, jwt
from serializers import marsh

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://message:message@localhost:5432/message_db'

db.init_app(app)
marsh.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(auth_bp)


if __name__ == '__main__':
    app.run(debug=True, port=9000)
