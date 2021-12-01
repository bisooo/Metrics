from django.shortcuts import render, redirect


def typography(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'typography.html')
