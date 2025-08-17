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
from django.urls import path
from messagesApp.views import poll_messages
from lobby.views import home_page
from smartIntents.views import smart_home_fulfillment
from django.views.generic import RedirectView
from users.views import login, callback

urlpatterns = [
    path('home/', home_page, name="home"),
    path('', RedirectView.as_view(pattern_name="home")),
    path("admin/login/", login, name="login"),
    path("auth/callback/", callback, name="callback"),
    path('admin/', admin.site.urls),
    path("api/poll-messages/", poll_messages, name="poll_messages"),
    path('smarthome/fulfillment/', smart_home_fulfillment, name='smart_home_fulfillment')
]

admin.site.site_header = 'MessageBridge Administration'
admin.site.index_title = 'Entity Management'
admin.site.site_title = 'MessageBridge Admin'
