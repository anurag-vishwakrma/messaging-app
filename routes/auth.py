# import requests
from flask import Blueprint, request, jsonify
# from marshmallow import ValidationError
import logging

from extension import db
from models.user import User

from serializers import UserSchema

auth_bp = Blueprint('auth', __name__, url_prefix='/api/user')

user_schema = UserSchema()


# @message_bp.errorhandler(ValidationError)
# def handle_validation_error(e):
#     return jsonify({
#         'status': 'error',
#         'data': [],
#         'message': e.messages,
#         'code': 400
#     }), 400


@auth_bp.route('/', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.get_json())
        msg_data = User(**data)
        db.session.add(msg_data)
        db.session.commit()
        return jsonify({
            "status": "success",
            "data": user_schema.dump(msg_data),
            "message": "User created successfully",
            "code": 201,
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "code": 400
        }), 400
