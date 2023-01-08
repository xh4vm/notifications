from django.shortcuts import HttpResponse

# from django.shortcuts import render


def home(request):
    return HttpResponse('<h1>MOVIES PROJECT!</h1>')
