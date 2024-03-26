import os
import django
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accounting_system.settings")
django.setup()
fake = Faker()

import random
from django.contrib.auth.models import User
from applications.requests.models import Involved
from applications.teams.models import Team
from datetime import datetime, timedelta
from api.sharepoint_api import SharePointAPI


"""
README:
- Delete the current database sqlite3
- Make migrations with 'py manage.py makemigrations' and 'py manage.py migrate' commands
- Execute the python script with 'py generate.py shell'
    - If you do not have permissions to execute scripts, open PowerShell as administrator and execute 'Set-ExecutionPolicy Unrestricted'
    - Now execute the command, this will generate sample data for the current models
- Select all code written by Playermast86, delete it and add it to the gitignore file.
"""

EXCEL_FILE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "djangoproyect/static/requests/emulation/requests_database.xlsx",
)

# print(EXCEL_FILE_PATH)

sharepoint_api = SharePointAPI(EXCEL_FILE_PATH)


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
for _ in range(10):
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
for _ in range(1):
    email = fake.email()
    name = fake.name()
    inv = Involved.objects.create(email=email, name=name)
    involved.append(inv)

# Create Requests and Traceability
for i in range(2):
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
    assigned_users = random.sample(users, random.randint(1, 3))

    data = {
        "document": document,
        "applicant": applicant,
        "manager": manager,
        "initial_date": initial_date,
        "final_date": final_date,
        "past_days": past_days,
        "description": description,
        "title": title,
        "status": status,
        "req_type": req_type,
        "assigned_users": assigned_users,
    }

    print(data)
    status_code = sharepoint_api.create_data(data)
    if status_code == 201:
        print("Working")
    else:
        print(f"Error")

    # traceability = Traceability.objects.create(
    #     involved=random.choice(involved),
    #     request=sharepoint_api.obtain_single_data(1),
    #     date=fake.date_time_between(start_date="-30d", end_date="+3d"),
    # )
