from functools import wraps

import jwt
from django.http import HttpResponseForbidden
from ninja.security import HttpBearer

from feedback import settings
from users.models import UserProfile


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        user_id = payload.get('id')
        try:
            return UserProfile.objects.get(id=user_id)
        except UserProfile.DoesNotExist:
            return None


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            if not request.auth.has_perm(permission):
                return HttpResponseForbidden("You do not have permission to perform this action.")
            return func(request, *args, **kwargs)
        return wrapped
    return decorator
