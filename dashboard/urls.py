from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),

    # Email
    path("inbox/", views.inbox, name="inbox"),
]
