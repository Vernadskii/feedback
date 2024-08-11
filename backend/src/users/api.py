from ninja import Router

from users.models import UserProfile
from users.api_schemas import UserSchema, LoginSchema, RegisterSchema
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from ninja.errors import HttpError

router = Router()


@router.post("/login", response={200: UserSchema, 401: str})
def login(request, payload: LoginSchema):
    user = authenticate(email=payload.email, password=payload.password)

    if user is not None:
        # If authentication is successful, return the user data
        return user
    else:
        # If authentication fails, return a 401 Unauthorized error
        raise HttpError(401, "Invalid email or password")


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
        return 201, user  # Return the created user, which will be serialized by UserSchema
    except ValidationError as e:
        raise HttpError(400, str(e))
