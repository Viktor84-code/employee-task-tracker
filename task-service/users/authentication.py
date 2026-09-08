from datetime import datetime, timezone

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings

from .models import User


class StatelessJWTAuthentication(JWTAuthentication):
    """
    Validates the JWT issued by auth-service (shared SECRET_KEY) and builds
    the request user from the token claims without a database lookup.
    """

    def get_user(self, validated_token):
        user_id = validated_token.get(api_settings.USER_ID_CLAIM)
        if user_id is None:
            return None

        user = User(pk=user_id)
        user.username = validated_token.get('username', f'user-{user_id}')
        user.email = validated_token.get('email', '')
        user.is_active = True
        iat = validated_token.get('iat')
        user.date_joined = (
            datetime.fromtimestamp(iat, tz=timezone.utc)
            if iat is not None
            else datetime.now(timezone.utc)
        )
        return user