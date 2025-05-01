from django.shortcuts import render

def home(request):
    """
    Renders the home page of the application.
    :param request:
    :return:
    """
    return render(request, "main/home.html")
