from django.shortcuts import render


def icons(request):
    return render(request, 'icons.html')
