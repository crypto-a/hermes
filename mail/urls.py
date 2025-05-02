from django.urls import path
from . import views

app_name = "mail"

urlpatterns = [
    path("connect/<slug:provider>/", views.start_oauth, name="start_oauth"),
    path("callback/<slug:provider>/", views.oauth_callback, name="oauth_callback"),
    path("api/messages/<int:account_id>/", views.messages_api, name="messages_api"),
]
