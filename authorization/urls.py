from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/$', views.log_in, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.log_out, name='logout')
]