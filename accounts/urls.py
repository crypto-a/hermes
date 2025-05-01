# auth/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", auth_views.LogoutView.as_view(next_page="main:home"), name="logout"),
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate"),
    path("settings/", views.profile_view, name="settings"),
]
