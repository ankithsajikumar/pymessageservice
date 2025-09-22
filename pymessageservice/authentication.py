import jwt
from jwt import PyJWKClient, InvalidTokenError
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from .constants import JWKS_CACHE_LIFE_SPAN


class JWTAuthentication(BaseAuthentication):
    """
    Authenticate requests using Bearer JWT access tokens validated via JWKS.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  # No credentials, let DRF handle as anonymous

        token = auth_header.split(" ")[1]

        try:
            # Get JWKS from cache or fetch from the endpoint
            jwks_url = f"{settings.SSO_BASE_URL}/o/.well-known/jwks.json"
            jwks_client = PyJWKClient(jwks_url, cache_keys=True)
            signing_key = jwks_client.get_signing_key_from_jwt(token)

            payload = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience=settings.SSO_AUDIENCE,
                issuer=settings.SSO_BASE_URL,
            )
        except InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f"Invalid token: {str(e)}")
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Token validation error: {str(e)}")

        user = self._get_user_from_claims(payload)
        return (user, payload)

    def _get_user_from_claims(self, claims):
        """
        Optionally map sub/client_id to Django user model.
        For now return a simple object with .is_authenticated = True.
        """
        from django.contrib.auth.models import AnonymousUser
        from django.contrib.auth import get_user_model

        User = get_user_model()
        sub = claims.get("sub")

        try:
            return User.objects.get(username=sub)
        except User.DoesNotExist:
            # Return a dummy "stateless user"
            user = AnonymousUser()
            user.username = sub
            return user
