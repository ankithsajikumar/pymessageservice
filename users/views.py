from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from requests_oauthlib import OAuth2Session
from django.contrib.auth import login as auth_login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User

def login(request):
    oauth = OAuth2Session(
        settings.SSO_CLIENT_ID,
        redirect_uri=settings.SSO_REDIRECT_URI,
        scope=["read", "write"]
    )
    authorization_url, state = oauth.authorization_url(f"{settings.SSO_BASE_URL}/o/authorize/")
    request.session['state'] = state
    return redirect(authorization_url)

def callback(request):
    state = request.session.get('state')
    if not state:
        # Handle missing state gracefully
        return redirect('/admin/login/?error=missing_state')
    oauth = OAuth2Session(
        settings.SSO_CLIENT_ID,
        redirect_uri=settings.SSO_REDIRECT_URI,
        state=state
    )
    token = oauth.fetch_token(
        f"{settings.SSO_BASE_URL}/o/token/",
        client_secret=settings.SSO_CLIENT_SECRET,
        authorization_response=request.build_absolute_uri()
    )

    resp = oauth.get(f"{settings.SSO_BASE_URL}/api/auth/me/")
    user_info = resp.json()

    user, created = User.objects.get_or_create(
        username=user_info["username"],
        defaults={
            "email": user_info["email"],
            "first_name": user_info["first_name"],
            "last_name": user_info["last_name"],
            "is_staff": user_info.get("is_staff", False),
            "is_superuser": user_info.get("is_superuser", False)
        }
    )

    auth_login(request, user)
    return redirect("/admin/")

# Test endpoint, to be removed
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    claims = request.auth
    return JsonResponse({
        "message": "Authorized",
        "user": request.user.username,
        "scopes": claims.get("scope", "").split(),
    })
