from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),

    # Email
    path("inbox/", views.inbox, name="inbox"),

    # Account management
    path("add_account/", views.add_account, name="add_account"),
]
