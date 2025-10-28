from django.db import models

class TaskManager(models.Manager):
    def open_tasks(self):
        return self.filter(status='open')

    def completed_tasks(self):
        return self.filter(status='completed')
