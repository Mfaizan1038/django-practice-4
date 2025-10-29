from django.db import models
from django.contrib.auth.models import User
from home.manager import TaskManager
from .base_models import TimeStampedModel  


class Profile(TimeStampedModel):
    class Role(models.TextChoices):
        MANAGER = 'manager', 'Manager'
        QA = 'qa', 'QA Engineer'
        DEVELOPER = 'developer', 'Developer'
        DESIGNER = 'designer', 'Designer'
        OTHER = 'other', 'Other'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OTHER)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


class Project(TimeStampedModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    team_members = models.ManyToManyField(User, related_name='projects')

    def __str__(self):
        return self.title


class Task(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = 'open', 'Open'
        WORKING = 'working', 'Working'
        REVIEW = 'review', 'Review'
        AWAITING_RELEASE = 'awaiting_release', 'Awaiting Release'
        WAITING_QA = 'waiting_qa', 'Waiting QA'

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')

    custom_object = TaskManager()

    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"


class Document(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='documents/')
    version = models.CharField(max_length=20)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return f"{self.name} (v{self.version})"


class Comment(TimeStampedModel):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"
