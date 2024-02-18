import os
from extension import db
from flask import Blueprint, request, jsonify, session
from models.user import User
from serializers import UserSchema, UserUpdateSchema
from passlib.hash import sha256_crypt
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timedelta, timezone
from decorators import public_endpoint
import logging
from sqlalchemy import func

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


user_schema = UserSchema()
user_update_schema = UserUpdateSchema()


@auth_bp.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify({
        'status': 'error',
        'data': [],
        'message': e.messages,
    }), 400


@auth_bp.route('/auth/change-password', methods=['POST'])
def change_password():
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if confirm_password != new_password:
            raise Exception("New-password and Confirm-password does not match")
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user and sha256_crypt.verify(current_password, user.password):
            setattr(user, 'password', sha256_crypt.encrypt(new_password))
            setattr(user, 'is_invite_accepted', True)
            db.session.commit()
            return jsonify({
                "status": "success",
                "data": [],
                "message": "password updated successfully",
            }), 200
        else:
            return jsonify({
                "status": "error",
                "data": [],
                "message": {"data": "Invalid Current Password"},
            }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "data": [],
            "message": {"data": str(e)},
        }), 400


@auth_bp.route('/auth', methods=['GET'])
def get_logged_in_user():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user:
            return jsonify({
                "status": "success",
                "data": user_schema.dump(user),
                "message": "Fetched User data successfully",
            }), 200
        else:
            return jsonify({
                "status": "error",
                "data": [],
                "message": {"data": "User not found"},
            }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "data": [],
            "message": {"data": str(e)},
        }), 400


@auth_bp.route('/auth', methods=['PUT'])
@jwt_required()
def update_logged_in_user():
    try:
        user_id = get_jwt_identity()
        schema = UserUpdateSchema()
        request_data = request.get_json()
        user_data = schema.load(request_data)
        # user_data = request.get_json()
        if user_data.get('first_name') and user_data.get('last_name'):
            user_data['display_name'] = f"{user_data.get('first_name')} {user_data.get('last_name')}"
        user = User.query.get(user_id)
        if user:
            for key, value in user_data.items():
                if key == 'password':
                    continue
                setattr(user, key, value)
            db.session.commit()
            return jsonify({
                "status": "success",
                "data": user_schema.dump(user),
                "message": "User updated successfully",
            }), 200
        return jsonify({
            "status": "error",
            "data": [],
            "message": {"data": "User not found"},
        }), 404
    except ValidationError as e:
        raise e
    except Exception as e:
        return jsonify({
            "status": "error",
            "data": [],
            "message": {"data": str(e)},
        }), 400


@auth_bp.route("/auth/refresh-token", methods=["GET"])
@jwt_required(refresh=True)
def refresh_access_token():
    try:
        user_id = get_jwt_identity()
        access_token = create_access_token(identity=user_id, expires_delta=timedelta(days=1))
        data = {
            "id": user_id,
            "token": access_token,
        }
        return jsonify({
            "status": "success",
            # "access_token": token,
            "data": data,
            "message": "Token generated successfully",
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "data": [],
            "message": {"data": str(e)},
        }), 400


@auth_bp.route('/login', methods=['POST'])
@public_endpoint
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        # user = db.session.query(User).filter_by(email=email).first()
        user = db.session.query(User).filter(func.lower(User.email) == func.lower(email)).first()
        if user and user.password in [None, "", '']:
            return jsonify({
                "status": "error",
                "data": [],
                "message": {"data": "Invalid Username/Password"},
            }), 400
        elif user and sha256_crypt.verify(password, user.password):
            token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(days=1))
            data = {
                "id": user.id,
                "token": token,
                "refresh_token": refresh_token
            }
            return jsonify({
                "status": "success",
                # "access_token": token,
                "data": data,
                "message": "User Logged in Successfully",
            }), 200
        else:
            return jsonify({
                "status": "error",
                "data": [],
                "message": {"data": "Invalid Username/Password"},
            }), 400
    else:
        return jsonify({
            "status": "error",
            "data": [],
            "message": {"data": "Invalid Request"},
        }), 400


