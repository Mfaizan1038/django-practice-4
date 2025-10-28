from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from home.models import Profile, Project, Task, Document, Comment
from faker import Faker
import random
from datetime import timedelta, date

fake = Faker()


class Command(BaseCommand):
    help = "Generate fake data for the ticket system"

    def handle(self, *args, **kwargs):
        
        roles = ['manager', 'qa', 'developer', 'designer']

        self.stdout.write("Creating Users and Profiles...")
        users = []
        for i in range(10):
            username = fake.user_name()
            user = User.objects.create_user(
                username=username,
                email=fake.email(),
                password='password123'
            )
            Profile.objects.create(
                user=user,
                role=random.choice(roles),
                contact_number=fake.phone_number()
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS(f" Created {len(users)} users."))

        
        self.stdout.write("Creating Projects...")
        projects = []
        for i in range(5):
            project = Project.objects.create(
                title=fake.bs().title(),
                description=fake.text(max_nb_chars=150),
                start_date=fake.date_between(start_date='-1y', end_date='-6m'),
                end_date=fake.date_between(start_date='-5m', end_date='today')
            )
           
            project.team_members.set(random.sample(users, k=random.randint(3, 6)))
            projects.append(project)
        self.stdout.write(self.style.SUCCESS(f"Created {len(projects)} projects."))

       
        statuses = ['open', 'working', 'review', 'awaiting_release', 'waiting_qa']
        self.stdout.write("Creating Tasks...")
        tasks = []
        for project in projects:
            for i in range(random.randint(5, 10)):
                task = Task.objects.create(
                    title=fake.sentence(nb_words=4),
                    description=fake.text(max_nb_chars=200),
                    status=random.choice(statuses),
                    project=project,
                    assignee=random.choice(users)
                )
                tasks.append(task)
        self.stdout.write(self.style.SUCCESS(f"Created {len(tasks)} tasks."))

       
        self.stdout.write("Creating Documents...")
        for project in projects:
            for i in range(random.randint(1, 3)):
                Document.objects.create(
                    name=fake.file_name(),
                    description=fake.text(max_nb_chars=100),
                    file='documents/sample.pdf',  
                    version=f"{random.randint(1, 3)}.{random.randint(0, 9)}",
                    project=project
                )
        self.stdout.write(self.style.SUCCESS("Documents created."))


        self.stdout.write("Creating Comments...")
        for task in tasks:
            for i in range(random.randint(1, 5)):
                Comment.objects.create(
                    text=fake.sentence(nb_words=10),
                    author=random.choice(users),
                    task=task,
                    project=task.project
                )
        self.stdout.write(self.style.SUCCESS("Comments created."))

        self.stdout.write(self.style.SUCCESS(" Fake data generation complete!"))
