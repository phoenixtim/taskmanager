from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def log_in(request):
    if len(request.POST) == 0:
        return render(request, 'authorization/login.html')
    else:
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('my_task_manager:main'))
        else:
            return render(request, 'authorization/login.html', {
                'error_message': "Wrong username or password!"
            })


def register(request):
    if len(request.POST) == 0:
        return render(request, 'authorization/register.html')
    else:
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            User.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse('my_task_manager:main'))
        else:
            return render(request, 'authorization/register.html', {
                'error_message': "User is already exist! Choose another login."
            })


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('my_task_manager:index'))
