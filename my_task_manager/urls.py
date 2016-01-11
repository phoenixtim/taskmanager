from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^main/$', views.MainView.as_view(), name='main'),
    url(r'^tasks/(?P<pk>[0-9]+)/update/$', views.update_task_view,
        name='update_task_view'),
    url(r'^tasks/create_task/$', views.create_task, name='create_task'),
    url(r'^tasks/(?P<pk>[0-9]+)/update_task/$', views.update_task,
        name='update_task'),
    url(r'^tasks/(?P<pk>[0-9]+)/$', views.TaskDetailView.as_view(),
        name='task_detail'),
]