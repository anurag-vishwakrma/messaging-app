from flask import Blueprint, request, jsonify
from extension import db
from models.user import User
from passlib.hash import sha256_crypt
from serializers import UserSchema
from decorators import public_endpoint

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

user_schema = UserSchema()


@user_bp.route('/', methods=['POST'])
@public_endpoint
def create_user():
    try:
        data = user_schema.load(request.get_json())
        if data.get('password'):
            data['password'] = sha256_crypt.encrypt(data.get('password'))
        if data.get('first_name') and data.get('last_name'):
            data['display_name'] = f"{data.get('first_name')} {data.get('last_name')}"
        user_data = User(**data)
        db.session.add(user_data)
        db.session.commit()
        return jsonify({
            "status": "success",
            "data": user_schema.dump(user_data),
            "message": "User created successfully",
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400
