from urllib import request
from django.http import HttpResponse



def django_hello(request) -> HttpResponse:
    return HttpResponse(
        "<h1>Greetings from the Django APP!!! :)</h1>"
    )

def user_hello(request):
    name = "Svetlana"
    return HttpResponse(
        f"<h2>Greetings {name}!!! :)</h2>"
    )