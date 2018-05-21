from django.http.response import HttpResponse


def index(request):
        return HttpResponse(content=b"FRONTEND SERVICE")
