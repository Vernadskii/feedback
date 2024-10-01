from ninja import Schema


class UserSchema(Schema):
    id: int | None
    first_name: str
    last_name: str
    job_title: str
    email: str


class UserUpdateSchema(Schema):
    email: str | None
    first_name: str | None
    last_name: str | None
    job_title: str | None
    email: str | None


class LoginSchema(Schema):
    email: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "admin@admin.com",
                    "password": "admin",
                }
            ]
        }
    }


class RegisterSchema(Schema):
    email: str
    password: str


class TokenSchema(Schema):
    token: str
