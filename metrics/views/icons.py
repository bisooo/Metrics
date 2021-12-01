from django.shortcuts import render, redirect


def icons(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'icons.html')
