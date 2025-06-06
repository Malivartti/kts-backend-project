from app.web.schemes import OkResponseSchema
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.Str()


class UserAuthSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


class UserResponseSchema(OkResponseSchema):
    data = fields.Nested(UserSchema)
