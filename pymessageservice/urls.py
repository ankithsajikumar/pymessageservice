"""pymessageservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path
from django_sso_client_oauth import views as sso_views
from messagesApp.views import poll_messages
from smartIntents.views import smart_home_fulfillment
from django.http import HttpResponseRedirect

def home_redirect(request):
    return HttpResponseRedirect(settings.HOME_URL)

urlpatterns = [
    path('', home_redirect),
    path("admin/login/", sso_views.login, name="login"),
    path("auth/callback/", sso_views.callback, name="callback"),
    path('admin/', admin.site.urls),
    path("api/poll-messages/", poll_messages, name="poll_messages"),
    path('smarthome/fulfillment/', smart_home_fulfillment, name='smart_home_fulfillment')
]

admin.site.site_header = 'MessageBridge Administration'
admin.site.index_title = 'Entity Management'
admin.site.site_title = 'MessageBridge Admin'
