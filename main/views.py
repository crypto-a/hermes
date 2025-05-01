from django.shortcuts import render, redirect

def index(request):
    """
    Renders the index page of the application.
    :param request:
    :return:
    """
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    return redirect("/home")

def home(request):
    """
    Renders the home page of the application.
    :param request:
    :return:
    """
    return render(request, "main/home.html")
