from flask_marshmallow import Marshmallow
from models.user import User
from models.message import Message
from marshmallow import Schema, fields, validate, validates_schema, ValidationError, validates

marsh = Marshmallow()


class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

    password = fields.Str(load_only=True)


class UserUpdateSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

    password = fields.Str(load_only=True)
    email = fields.Email(required=False)

    @validates_schema
    def validate_email(self, data):
        # Check for uniqueness of the name and contact_number
        user_id = data.get("id")
        email = data.get("email")
        contact_number = data.get("contact_number")
        errors = {}
        if email and User.query.filter(User.email == email, User.id != user_id).first():
            errors['email'] = ['User with this email already exists.']
        if contact_number and User.query.filter(User.contact_number == contact_number, User.id != user_id).first():
            errors['contact_number'] = ['User with this Contact_no already exists.']
        if errors:
            raise ValidationError(errors)


class MessageSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        include_fk = True
