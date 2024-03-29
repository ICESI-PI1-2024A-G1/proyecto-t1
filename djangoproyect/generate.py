import json
import os
import django
from django.conf import settings
from faker import Faker
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accounting_system.settings")
django.setup()
fake = Faker()

import random
from django.contrib.auth import get_user_model
from applications.requests.models import Involved, Traceability
from applications.teams.models import Team
from datetime import datetime, timedelta
from api.sharepoint_api import SharePointAPI

User = get_user_model()

"""
README:
- Add to the .env file the ADMIN_PASSWORD and ADMIN_EMAIL fields
- Delete the current database sqlite3
- Make migrations with 'py manage.py makemigrations' and 'py manage.py migrate' commands
- Execute the python script with 'py generate.py shell'
    - If you do not have permissions to execute scripts, open PowerShell as administrator and execute 'Set-ExecutionPolicy Unrestricted'
    - Now execute the command, this will generate sample data for the current models
- Select all code written by Playermast86, delete it and add it to the gitignore file.
"""

EXCEL_FILE_PATH = os.path.join(
    settings.BASE_DIR,
    "static",
    "requests",
    "emulation",
    "requests_database.xlsx",
)

# print(EXCEL_FILE_PATH)

sharepoint_api = SharePointAPI(EXCEL_FILE_PATH)
sharepoint_api.clear_db()

# Create superuser

if not User.objects.filter(id=0).exists():
    admin = User.objects.create_user(
        id=os.getenv("ADMIN_PASSWORD"),
        username="admin",
        email=os.getenv("ADMIN_EMAIL"),
        password=os.getenv("ADMIN_PASSWORD"),
        first_name="Accounting",
        last_name="Admin",
        is_staff=True,
        is_superuser=True,
        is_leader=True,
    )
    admin.save()
    print(admin)


# Create users
users = []
for _ in range(10):
    id = str(random.randint(1000000, 99999999))
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = id
    email = fake.email()
    password = "12345678"
    user = User.objects.create_user(
        id=id,
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    print(f"User created: {user.username}")
    users.append(user)


# Create teams, leaders and add members
teams = []
leaders = []
for _ in range(5):
    name = fake.company()
    description = fake.text()
    leader = random.choice(
        User.objects.exclude(id__in=[leader.id for leader in leaders])
    )
    # leader = random.choice(users)
    leader.is_leader = True
    leader.save()
    leaders.append(leader)
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
for i in range(10):

    status_options = [
        "EN PROCESO",
        "APROBADO - CENCO",
        "RECHAZADO - CENCO",
        "APROBADO - DECANO",
        "RECHAZADO - DECANO",
        "PAGADO - CONTABILIDAD",
        "RECHAZADO - CONTABILIDAD",
        "CERRADO",
    ]
    initial_date = fake.date_between(start_date="-30d", end_date="+4d")
    final_date = initial_date + timedelta(days=random.randint(1, 30))

    data = {
        "status": random.choice(status_options),
        "manager": random.choice(users),
        "team": random.choice(teams).id,
        "initial_date": initial_date.strftime("%d-%m-%Y"),
        "final_date": final_date.strftime("%d-%m-%Y"),
        "fullname": fake.name(),
        "faculty": fake.company(),
        "document": fake.random_number(digits=10),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "CENCO": fake.word(),
        "reason": fake.text(),
        "bank": fake.company(),
        "account_type": random.choice(["Ahorros", "Corriente"]),
        "health_provider": fake.company(),
        "pension_fund": fake.company(),
        "arl": fake.company(),
        "contract_value": fake.random_number(digits=7),
        "is_one_time_payment": random.choice([True, False]),
    }

    sharepoint_api.create_data(data)

t_request = sharepoint_api.get_all_requests()
t_request = json.loads(t_request.content)
for i in range(len(t_request)):
    user = User.objects.first()
    temp_r = t_request[random.randint(0, len(t_request) - 1)]
    new_id = temp_r["id"]
    traceability = Traceability.objects.create(
        modified_by=user,
        request=new_id,
        date=fake.date_time_between(start_date="-30d", end_date="+3d"),
        reason=fake.text(),
        prev_state=temp_r["status"],
        new_state=random.choice(status_options),
    )
