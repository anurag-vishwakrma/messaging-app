from flask import Blueprint, request, jsonify
from extension import db
from models.message import Message
from serializers import MessageSchema

message_bp = Blueprint('message', __name__, url_prefix='/api/message')

message_schema = MessageSchema()


@message_bp.route('/', methods=['POST'])
def create_msg():
    try:
        data = message_schema.load(request.get_json())
        user_data = Message(**data)
        db.session.add(user_data)
        db.session.commit()
        return jsonify({
            "status": "success",
            "data": message_schema.dump(user_data),
            "message": "Message created successfully",
        }), 201

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
        }), 400
