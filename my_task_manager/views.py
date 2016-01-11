from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


"""
class CreateTaskView(generic.DetailView):
    template_name = 'my_task_manager/create_task.html'
    context_object_name = 'users_list'

    def get_queryset(self):
        return User.objects.all()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CreateTaskView, self).dispatch(*args, **kwargs)
"""


"""
class UpdateTaskView(generic.DetailView):
    model = Task
    template_name = 'my_task_manager/update_task.html'
    #context_object_name = 'users_list'

    def get_context_data(self, **kwargs):
        return User.objects.all()
    def get_queryset(self):
        users_list = {User.objects.all()}
        return User.objects.order_by('username')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateTaskView, self).dispatch(*args, **kwargs)
"""


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
