from flask_marshmallow import Marshmallow
from models.user import User
from marshmallow import Schema, fields, validate, validates_schema, ValidationError, validates

marsh = Marshmallow()


class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True

