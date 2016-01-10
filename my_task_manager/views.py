from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Task


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('my_task_manager:main'))
    else:
        return HttpResponseRedirect(reverse('authorization:login'))


class MainView(generic.ListView):
    template_name = 'my_task_manager/main.html'
    context_object_name = 'user_tasks'

    def get_queryset(self):
        """
        Return all tasks for current user that are not finished.
        """
        return Task.objects.filter(
                responsible=self.request.user
        ).order_by('date_created')