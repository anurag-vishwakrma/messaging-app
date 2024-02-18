import os
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from routes.auth import auth_bp
from routes.user import user_bp
from routes.message import message_bp
from extension import db, jwt
from serializers import marsh
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = (f"postgresql+psycopg2://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}"
                                         f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
port = int(os.getenv("SERVICE_PORT", 5000))

db.init_app(app)
marsh.init_app(app)
jwt.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(message_bp)


@app.before_request
def check_token():
    """
    Checking access token for in every request.
    """
    if (request.endpoint and 'static' not in request.endpoint
            and not getattr(app.view_functions[request.endpoint], 'is_public', False)):
        try:
            verify_jwt_in_request()
        except NoAuthorizationError as e:
            app.logger.exception(e)
            return jsonify({
                "status": "error",
                "message": {"data": f"{e}"},
                "data": [],
                "code": 401
            }), 401


if __name__ == '__main__':
    app.run(debug=True, port=port)
