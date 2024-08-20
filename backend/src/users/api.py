import datetime as dt

import jwt
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ninja import Router
from ninja.errors import HttpError
from ninja.security import HttpBearer

from feedback import settings
from users.api_schemas import (
    LoginSchema,
    RegisterSchema,
    TokenSchema,
    UserSchema,
)
from users.models import UserProfile


router = Router(tags=["users"])


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return payload  # Return the payload (can be a user identifier or custom data)


@router.post("/login", response={200: TokenSchema, 401: str})
def login(request, payload: LoginSchema):
    user = authenticate(email=payload.email, password=payload.password)

    if user is not None:
        token = jwt.encode(
            {
                'id': user.id,
                'exp': dt.datetime.utcnow() + dt.timedelta(hours=24),  # Token valid for 24 hours
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )
        return {"token": token}
    else:
        # If authentication fails, return a 401 Unauthorized error
        raise HttpError(401, "Invalid email or password")  # noqa:  WPS503, WPS432


@router.post("/register", response={201: UserSchema, 400: str})
def register(request, payload: RegisterSchema):
    # Check if the email already exists
    if UserProfile.objects.filter(email=payload.email).exists():
        raise HttpError(400, "Email already exists")

    # Create the user
    try:
        user = UserProfile.objects.create_user(
            email=payload.email,
            password=payload.password,
        )
        user.save()
    except ValidationError as ex:
        raise HttpError(400, str(ex))

    return 201, user  # Return the created user, which will be serialized by UserSchema


@router.get("/protected", response={200: UserSchema}, auth=AuthBearer())
def protected_route(request):
    # Assuming the payload contains the user's ID, you can retrieve the user
    user_id = request.auth['id']
    return UserProfile.objects.get(id=user_id)
