import os
import django
import random
from faker import Faker
from django.contrib.auth.models import User
from applications.requests.models import Involved, Requests, Traceability
from applications.teams.models import Team
from datetime import datetime, timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accounting_system.settings")
django.setup()
fake = Faker()

"""
README:
- Delete the current database sqlite3
- Make migrations with 'py manage.py makemigrations' and 'py manage.py migrate' commands
- Execute the python script with 'py generate.py shell'
    - If you do not have permissions to execute scripts, open PowerShell as administrator and execute 'Set-ExecutionPolicy Unrestricted'
    - Now execute the command, this will generate sample data for the current models
- Select all code written by Playermast86, delete it and add it to the gitignore file.
"""


# Create users
users = []
for _ in range(10):
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = fake.user_name()
    email = fake.email()
    password = fake.password()
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    users.append(user)

# Choose one user to be staff
staff_user = random.choice(users)
staff_user.is_staff = True
staff_user.save()

# Create teams and add members
teams = []
for _ in range(5):
    name = fake.company()
    description = fake.text()
    leader = random.choice(users)
    team = Team.objects.create(name=name, description=description, leader=leader)

    # Seleccionar miembros para el equipo (excluyendo al líder)
    team_members = random.sample(
        [user for user in users if user != leader], random.randint(3, 5)
    )
    team.members.add(*team_members)

    teams.append(team)


# Create Involved
involved = []
for _ in range(15):
    email = fake.email()
    name = fake.name()
    inv = Involved.objects.create(email=email, name=name)
    involved.append(inv)

# Create Requests and Traceability
for _ in range(20):
    document = fake.file_name()
    applicant = random.choice(users)
    manager = random.choice(users)
    initial_date = fake.date_between(start_date="-30d", end_date="+4d")
    final_date = initial_date + timedelta(days=random.randint(1, 30))
    past_days = (datetime.now().date() - initial_date).days
    description = fake.text()
    title = fake.name()
    status = random.choice(["Pending", "Approved", "Rejected"])
    req_type = random.choice(["Type 1", "Type 2", "Type 3"])

    request = Requests.objects.create(
        document=document,
        applicant=applicant.username,
        manager=manager.username,
        initial_date=initial_date,
        final_date=final_date,
        past_days=past_days,
        status=status,
        type=req_type,
        description=description,
        title=title,
    )

    assigned_users = random.sample(users, random.randint(1, 3))
    request.assigned_users.add(*assigned_users)

    traceability = Traceability.objects.create(
        involved=random.choice(involved),
        request=request,
        date=fake.date_time_between(start_date="-30d", end_date="+3d"),
    )
