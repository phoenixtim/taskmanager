from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class ManagerTask(models.Manager):
    def create_task(self, responsible_name, text, creator_name,
                    date_created=timezone.now()):
        task = self.create(
                responsible=User.objects.get(username=responsible_name),
                text=text,
                creator=User.objects.get(username=creator_name),
                date_created=date_created
        )
        return task


class Task(models.Model):
    creator = models.ForeignKey(User, related_name='task_creator')
    responsible = models.ForeignKey(User, related_name='task_responsible')
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(null=True)
    completed = models.BooleanField(default=False)
    text = models.CharField(max_length=1000)

    objects = ManagerTask()

    def __str__(self):
        return self.text

    def set_complete(self):
        self.completed = True
        self.date_completed = timezone.now
