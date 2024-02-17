from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

jwt = JWTManager()
db = SQLAlchemy()


@jwt.expired_token_loader
def expired_token_token():
    return jsonify({
        "status": "error",
        "message": {"data": "Token has expired"},
        "data": [],
        "code": 401
    }), 401


@jwt.invalid_token_loader
def check_invalid_token(jwt_header):
    return jsonify({
        "status": "error",
        "message": {"data": f"{jwt_header}"},
        "data": [],
    }), 401


@jwt.unauthorized_loader
def check_unauthorized_token(jwt_header):
    return jsonify({
        "status": "error",
        "message": {"data": f"{jwt_header}"},
        "data": [],
    }), 401
