from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse
from requests_oauthlib import OAuth2Session
from django.contrib.auth import login as auth_login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Permission
import logging

from .models import User

logger = logging.getLogger(__name__)

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
    try:
        # Check if state exists in the session
        state = request.session.get('state')
        if not state:
            return redirect('/admin/login/?error=missing_state')

        # Initialize OAuth2 session
        oauth = OAuth2Session(
            settings.SSO_CLIENT_ID,
            redirect_uri=settings.SSO_REDIRECT_URI,
            state=state
        )

        # Fetch token from the SSO provider
        try:
            token = oauth.fetch_token(
                f"{settings.SSO_BASE_URL}/o/token/",
                client_secret=settings.SSO_CLIENT_SECRET,
                authorization_response=request.build_absolute_uri()
            )
        except Exception as e:
            logger.error(f"Error fetching token: {e}")
            return redirect('/admin/login/?error=token_fetch_failed')

        # Fetch user info from the SSO provider
        try:
            resp = oauth.get(f"{settings.SSO_BASE_URL}/api/auth/me/")
            resp.raise_for_status()  # Raise an error for non-200 responses
            user_info = resp.json()
        except Exception as e:
            logger.error(f"Error fetching user info: {e}")
            return redirect('/admin/login/?error=user_info_fetch_failed')

        # Normalize the username
        normalized_username = user_info.get("username", "").strip().lower()
        if not normalized_username:
            logger.error("Error: Missing username in user_info")
            return redirect('/admin/login/?error=missing_username')

        # Get or create the user
        try:
            user, created = User.objects.get_or_create(username=normalized_username)
        except Exception as e:
            logger.error(f"Error creating or fetching user: {e}")
            return redirect('/admin/login/?error=user_creation_failed')

        # Update user fields dynamically, excluding the username field
        for key, value in user_info.items():
            if key not in ["username", "id", "permissions"] and hasattr(user, key):
                try:
                    setattr(user, key, value)
                except Exception as e:
                    logger.error(f"Error updating field {key} for user {normalized_username}: {e}")

        # Save the updated user
        try:
            user.save()
        except Exception as e:
            logger.error(f"Error saving user {normalized_username}: {e}")
            return redirect('/admin/login/?error=user_save_failed')

        # Assign permissions to the user
        if "permissions" in user_info:
            try:
                user.user_permissions.clear()  # Clear existing permissions
                for permission_item in user_info["permissions"]:
                    permission = Permission.objects.filter(codename=permission_item["codename"]).first()
                    if permission:
                        user.user_permissions.add(permission)
                    else:
                        logger.debug(f"Permission with codename {permission_item} does not exist")
            except Exception as e:
                logger.error(f"Error assigning permissions to user {normalized_username}: {e}")

        # Log the user in
        try:
            auth_login(request, user)
        except Exception as e:
            logger.error(f"Error logging in user {normalized_username}: {e}")
            return redirect('/admin/login/?error=login_failed')

        return redirect("/admin/")

    except Exception as e:
        logger.error(f"Unexpected error in callback: {e}")
        return redirect('/admin/login/?error=unexpected_error')
    

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
