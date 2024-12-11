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
from django.urls import path, include
from oauth2_provider import urls as oauth2_urls
from messagesApp.views import receive_message, get_messages
from lobby.views import home_page
from smartIntents.views import smart_home_fulfillment
from smartDevices.views import create_device, get_device, update_device, delete_device
from django.views.generic import RedirectView

urlpatterns = [
    path('home/', home_page, name="home"),
    path('', RedirectView.as_view(pattern_name="home")),
    path('admin/', admin.site.urls),
    path('o/', include(oauth2_urls)),
    path("api/receive-message/", receive_message, name="receive_message"),
    path("api/get-messages/", get_messages, name="get_messages"),
    path('smarthome/fulfillment/', smart_home_fulfillment, name='smart_home_fulfillment'),
    path('device/create/', create_device, name='create_device'),
    path('device/<str:device_id>/', get_device, name='get_device'),
    path('device/<str:device_id>/update/', update_device, name='edit_device'),
    path('device/<str:device_id>/delete/', delete_device, name='delete_device'),
]
