from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
import datetime

from .models import Task


def index(request):
    """
    Site main page
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('my_task_manager:main'))
    else:
        return HttpResponseRedirect(reverse('authorization:login'))


class MainView(generic.ListView):
    template_name = 'my_task_manager/main.html'
    context_object_name = 'user_tasks'

    def get_queryset(self):
        """
        Return all tasks for current user that are not completed.
        """
        return Task.objects.filter(
            responsible=self.request.user,
            completed=False,
        ).order_by('date_created')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MainView, self).dispatch(*args, **kwargs)


@login_required
def update_task_view(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'my_task_manager/update_task.html', {
        'users_list': User.objects.all(),
        'task': task,
    })


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    responsible = request.POST['responsible']
    text = request.POST['text']

    task.creator = request.user
    task.responsible = User.objects.filter(username=responsible)[0]
    task.text = text
    task.save()

    return HttpResponseRedirect(reverse('my_task_manager:task_detail',
                                        args=(task.id,)))


@login_required
def create_task(request):
    if len(request.POST) == 0:
        return render(request, 'my_task_manager/create_task.html', context={
            'users_list': User.objects.all(),
        })
    else:
        responsible = request.POST['responsible']
        text = request.POST['text']
        task = Task.objects.create_task(
                creator_name=request.user.username,
                responsible_name=responsible,
                text=text
        )
        return HttpResponseRedirect(reverse('my_task_manager:task_detail',
                                            args=(task.id,)))


class TaskDetailView(generic.DetailView):
    model = Task
    template_name = 'my_task_manager/task_detail.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(TaskDetailView, self).dispatch(*args, **kwargs)


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.user != task.responsible:
        return render(request, 'my_task_manager/task_detail.html', {
            'error_message': "You can't complete another user task!",
        })
    else:
        task.date_completed = timezone.now()
        task.completed = True
        task.save()
        return HttpResponseRedirect(reverse('my_task_manager:main'))


@login_required
def all_tasks_view(request):
    if len(request.GET) != 0:
        # creator_name = request.GET['creator']
        creator = User.objects.filter(username=request.GET['creator'])
        # responsible_name = request.GET['responsible']
        responsible = User.objects.filter(username=request.GET['responsible'])
        is_created_from = request.GET.get('created_from', False)
        created_from = datetime.datetime(
                int(request.GET['created_from_year']),
                int(request.GET['created_from_month']),
                int(request.GET['created_from_day']),
                int(request.GET['created_from_hour']),
                int(request.GET['created_from_minute'])
        )
        is_created_to = request.GET.get('created_to', False)
        created_to = datetime.datetime(
                int(request.GET['created_to_year']),
                int(request.GET['created_to_month']),
                int(request.GET['created_to_day']),
                int(request.GET['created_to_hour']),
                int(request.GET['created_to_minute'])
        )
        is_finished_from = request.GET.get('finished_from', False)
        finished_from = datetime.datetime(
                int(request.GET['finished_from_year']),
                int(request.GET['finished_from_month']),
                int(request.GET['finished_from_day']),
                int(request.GET['finished_from_hour']),
                int(request.GET['finished_from_minute'])
        )
        is_finished_to = request.GET.get('finished_to', False)
        finished_to = datetime.datetime(
                int(request.GET['finished_to_year']),
                int(request.GET['finished_to_month']),
                int(request.GET['finished_to_day']),
                int(request.GET['finished_to_hour']),
                int(request.GET['finished_to_minute'])
        )
        finished = request.GET.get('finished', False)
        not_finished = request.GET.get('not_finished', False)

        tasks = Task.objects.all()
        if is_created_from == 'on':
            tasks = tasks.filter(date_created__gte=created_from)
        if is_created_to == 'on':
            tasks = tasks.filter(date_created__lte=created_to)
        if is_finished_from == 'on':
            tasks = tasks.filter(date_completed__gte=finished_from)
        if is_finished_to == 'on':
            tasks = tasks.filter(date_completed__lte=finished_to)
        if len(creator) != 0:
            tasks = tasks.filter(creator=creator[0])
        if len(responsible) != 0:
            tasks = tasks.filter(responsible=responsible[0])
        if finished is False:
            if not_finished == 'on':
                tasks = tasks.filter(completed=False)
        else:
            if not_finished is False:
                tasks = tasks.filter(completed=True)

        return render(request, 'my_task_manager/all_tasks.html', {
            'tasks_list': tasks.order_by('date_created'),
            'users_list': User.objects.all(),
        })
    else:
        return render(request, 'my_task_manager/all_tasks.html', {
            'tasks_list': Task.objects.order_by('date_created'),
            'users_list': User.objects.all(),
        })
