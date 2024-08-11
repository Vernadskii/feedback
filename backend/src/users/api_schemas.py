from ninja import Schema


class UserSchema(Schema):
    id: int
    first_name: str
    last_name: str
    email: str


class LoginSchema(Schema):
    email: str
    password: str


class RegisterSchema(Schema):
    email: str
    password: str
