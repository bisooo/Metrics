from django.shortcuts import render, redirect


def notifications(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'notifications.html')