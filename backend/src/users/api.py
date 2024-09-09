import datetime as dt
from http import HTTPStatus

import jwt
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import Http404
from ninja import Router
from ninja.errors import HttpError
from ninja.security import HttpBearer

from feedback import settings
from users.api_schemas import (
    LoginSchema,
    RegisterSchema,
    TokenSchema,
    UserSchema,
    UserUpdateSchema,
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
        raise HttpError(HTTPStatus.BAD_REQUEST, "Email already exists")

    # Create the user
    try:  # noqa: WPS229
        user = UserProfile.objects.create_user(
            email=payload.email,
            password=payload.password,
        )
        user.save()
    except ValidationError as ex:
        raise HttpError(HTTPStatus.BAD_REQUEST, str(ex))

    return 201, user  # Return the created user, which will be serialized by UserSchema


@router.get("/", response={200: list[UserSchema]}, auth=AuthBearer())
def get_users(request):
    return list(UserProfile.objects.all())


@router.get("/{user_id}", response={200: UserSchema, 404: str}, auth=AuthBearer())
def get_user(request, user_id: int):
    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        raise Http404(f"User with ID {user_id} not found.")
    return user


@router.patch("/{user_id}", response={200: UserSchema, 404: str}, auth=AuthBearer())
def update_user(request, user_id: int, payload: UserUpdateSchema):
    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        raise Http404(f"User with ID {user_id} not found.")

    # Apply the changes from the payload
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(user, attr, value)

    user.save()
    return user
