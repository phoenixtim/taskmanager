from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


"""
class User(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
"""


class Task(models.Model):
    creator = models.ForeignKey(User, related_name='task_creator')
    responsible = models.ForeignKey(User, related_name='task_responsible')
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField()
    completed = models.BooleanField(default=False)
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text

    def set_complete(self):
        self.completed = True
        self.date_completed = timezone.now
