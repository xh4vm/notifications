from django.shortcuts import HttpResponse

# from django.shortcuts import render


def home(request):
    return HttpResponse('<h3>This service is only for work with admin panel.</h3>')
