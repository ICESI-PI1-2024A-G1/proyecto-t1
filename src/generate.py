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
from apps.internalRequests.models import Traceability
from apps.teams.models import Team
from datetime import datetime, timedelta
from api.sharepoint_api import SharePointAPI
from apps.forms.models import *
from django.utils import timezone
import json
from django.db import transaction
from django.db.models import Max


def get_next_id():
    max_id1 = TravelAdvanceRequest.objects.all().aggregate(Max("id"))["id__max"] or 0
    max_id2 = AdvanceLegalization.objects.all().aggregate(Max("id"))["id__max"] or 0
    max_id3 = BillingAccount.objects.all().aggregate(Max("id"))["id__max"] or 0
    max_id4 = Requisition.objects.all().aggregate(Max("id"))["id__max"] or 0
    max_id5 = (
        TravelExpenseLegalization.objects.all().aggregate(Max("id"))["id__max"] or 0
    )
    return max(max_id1, max_id2, max_id3, max_id4, max_id5) + 1


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

# Clear contents
sharepoint_api = SharePointAPI(EXCEL_FILE_PATH)
sharepoint_api.clear_db()
Traceability.objects.all().delete()
Team.objects.all().delete()
User.objects.all().delete()
# Forms
TravelAdvanceRequest.objects.all().delete()
TravelExpenseLegalization_Table.objects.all().delete()
TravelExpenseLegalization.objects.all().delete()
AdvanceLegalization_Table.objects.all().delete()
AdvanceLegalization.objects.all().delete()
BillingAccount.objects.all().delete()
Requisition.objects.all().delete()

# Create superuser

if not User.objects.filter(id=0).exists():
    admin = User.objects.create_user(
        id=os.getenv("ADMIN_PASSWORD"),
        username="admin",
        email=os.getenv("ADMIN_EMAIL"),
        password=os.getenv("ADMIN_PASSWORD"),
        first_name="Accounting",
        last_name="Admin",
        is_superuser=True,
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
names = ["Contabilidad", "Lógistica", "Programacion académica", "Contratación"]
teams = []
leaders = []
for i in range(4):
    name = names[i]
    description = fake.text(max_nb_chars=100)
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

    # Asignar el permiso de "is_member" a los miembros del equipo
    for member in team_members:
        member.is_member = True
        member.save()

    team.members.add(*team_members)

    teams.append(team)

    # Create Requests and Traceability

faculty = [
    "Ciencias Administrativas y económicas",
    "Ingeniería, Diseño y Ciencias Aplicadas",
    "Ciencias Humanas",
    "Ciencias de la Salud",
]
banks = [
    "Banco de Bogotá",
    "Bancolombia",
    "Banco Davivienda",
    "Banco Popular",
    "Banco AV Villas",
    "Banco Caja Social",
    "Banco de Occidente",
    "Banco GNB Sudameris",
    "Banco Itaú",
    "Bancoomeva",
    "Banco Pichincha",
    "Banco Santander Colombia",
    "BBVA Colombia",
    "Citibank Colombia",
    "Scotiabank Colpatria",
    "Banco Finandina",
    "HSBC",
    "Citibank",
    "JPMorgan Chase",
    "Bank of America",
    "Barclays",
    "BNP Paribas",
    "Deutsche Bank",
    "UBS",
    "Santander",
    "Credit Suisse",
    "ING Group",
    "Goldman Sachs",
    "Morgan Stanley",
    "Wells Fargo",
    "Standard Chartered",
    "Banco Santander",
    "Royal Bank of Canada",
    "Banco Sabadell",
    "Banco Bilbao Vizcaya Argentaria (BBVA)",
    "The Bank of Tokyo-Mitsubishi UFJ",
]
eps = [
    "Sura",
    "Sanitas",
    "Famisanar",
    "Compensar",
    "Medimás",
    "Salud Total",
    "Coomeva",
    "Nueva EPS",
    "Aliansalud",
    "SOS",
    "Cafesalud",
    "Coosalud",
    "Savia Salud",
    "Mutual Ser",
    "Cruz Blanca",
    "Capital Salud",
    "Comfenalco",
    "Comfama",
    "Comfandi",
    "Comfasucre",
]
pension_fund = [
    "Porvenir",
    "Protección",
    "Colfondos",
    "Skandia",
    "Old Mutual",
    "Colpensiones",
    "Habitat",
    "Horizonte",
    "Crecer",
    "Fiduprevisora",
    "Cafam",
    "Confuturo",
    "CFA",
    "Fondo Nacional del Ahorro",
]

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

arls = [
    "Sura ARL",
    "Positiva ARL",
    "Colmena Seguros ARL",
    "Seguros Bolívar ARL",
    "Axa Colpatria ARL",
    "Liberty Seguros ARL",
    "Bolívar ARL",
    "Mapfre ARL",
    "Equidad Seguros ARL",
    "Seguros del Estado ARL",
    "Mundial de Seguros ARL",
    "La Previsora ARL",
    "Seguros Generales Suramericana ARL",
    "Seguros del Sur ARL",
    "Protección ARL",
]

documents = [
    "Cuenta de cobro",
    "Legalizacion",
    "Anticipo",
    "Viatico",
    "Factura",
    "Factura CEX",
    "Requisición",
]

for i in range(10):
    initial_date = fake.date_between(start_date="-30d", end_date="+4d")
    final_date = initial_date + timedelta(days=random.randint(1, 30))

    data = {
        "status": random.choice(status_options),
        "manager": random.choice(users),
        "team": random.choice(teams).id,
        "initial_date": initial_date.strftime("%d-%m-%Y"),
        "final_date": final_date.strftime("%d-%m-%Y"),
        "fullname": fake.name(),
        "faculty": random.choice(faculty),
        "document": random.choice(documents),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "CENCO": fake.random_number(digits=5),
        "bank": random.choice(banks),
        "account_type": random.choice(["Ahorros", "Corriente"]),
        "health_provider": random.choice(eps),
        "pension_fund": random.choice(pension_fund),
        "arl": random.choice(arls),
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
        prev_state=temp_r["status"],
        new_state=random.choice(status_options),
    )

requestStatus = ["PENDIENTE", "EN REVISIÓN", "DEVUELTO", "RECHAZADO"]


def create_fake_travel_request():
    expenses_dict = {
        "transportation": fake.random_int(min=50, max=500),
        "accommodation": fake.random_int(min=100, max=1000),
        "meals": fake.random_int(min=20, max=200),
        "other": fake.random_int(min=0, max=300),
    }

    request = TravelAdvanceRequest(
        request_date=fake.date_between(start_date="-30d", end_date="today"),
        final_date=fake.date_between(start_date="today", end_date="+30d"),
        traveler_name=fake.name(),
        id_person=fake.random_number(digits=8),
        member_name=fake.name(),
        dependence=fake.company(),
        cost_center=fake.random_int(min=1000, max=9999),
        destination_city=fake.city(),
        departure_date=fake.date_between(start_date="+1d", end_date="+60d"),
        return_date=fake.date_between(start_date="+61d", end_date="+120d"),
        travel_reason=fake.sentence(nb_words=6),
        currency=fake.currency_code(),
        signature_status=fake.random_element(
            elements=("Pendiente", "Aprobada", "Rechazada")
        ),
        bank=random.choice(banks),
        account_type=fake.random_element(elements=("Savings", "Checking")),
        account_number=fake.iban(),
        observations=fake.text(),
        team_id=fake.random_int(min=1, max=10),
    )
    request.set_expenses(expenses_dict)
    with transaction.atomic():
        request.id = get_next_id()
    request.save()


def create_fake_travel_expense_legalization():
    travel_expense = TravelExpenseLegalization(
        request_date=fake.date_between(start_date="-30d", end_date="today"),
        final_date=fake.date_between(start_date="today", end_date="+30d"),
        traveler_name=fake.name(),
        id_person=fake.random_number(digits=8),
        member_name=fake.name(),
        dependence=fake.company(),
        cost_center=fake.random_int(min=1000, max=9999),
        destination_city=fake.city(),
        departure_date=fake.date_between(start_date="+1d", end_date="+60d"),
        return_date=fake.date_between(start_date="+61d", end_date="+120d"),
        travel_reason=fake.text(),
        total1=fake.random_int(min=100, max=1000),
        total2=fake.random_int(min=100, max=1000),
        total3=fake.random_int(min=100, max=1000),
        advance_total1=fake.random_int(min=50, max=500),
        advance_total2=fake.random_int(min=50, max=500),
        advance_total3=fake.random_int(min=50, max=500),
        employee_balance1=fake.random_int(min=0, max=500),
        employee_balance2=fake.random_int(min=0, max=500),
        employee_balance3=fake.random_int(min=0, max=500),
        icesi_balance1=fake.random_int(min=0, max=500),
        icesi_balance2=fake.random_int(min=0, max=500),
        icesi_balance3=fake.random_int(min=0, max=500),
        signature_status=fake.boolean(),
        bank=random.choice(banks),
        account_type=fake.random_element(elements=("Savings", "Checking")),
        account_number=fake.iban(),
        observations=fake.text(),
        team_id=fake.random_int(min=1, max=10),
    )
    with transaction.atomic():
        travel_expense.id = get_next_id()
    travel_expense.save()

    # Crear varias entradas de ejemplo para TravelExpenseLegalization_Table asociadas
    for _ in range(
        fake.random_int(min=1, max=5)
    ):  # Puedes ajustar el rango según tus necesidades
        travel_info = TravelExpenseLegalization_Table(
            travel_info=travel_expense,
            category=fake.word(),
            provider=fake.company(),
            nit=fake.random_number(digits=10),
            concept=fake.sentence(),
            pesos=fake.random_int(min=100, max=1000),
            dollars=fake.random_int(min=50, max=500),
            euros=fake.random_int(min=50, max=500),
        )
        travel_info.save()


def create_fake_advance_legalization():
    advance_legalization = AdvanceLegalization(
        request_date=fake.date_between(start_date="-30d", end_date="today"),
        final_date=fake.date_between(start_date="today", end_date="+30d"),
        traveler_name=fake.name(),
        id_person=fake.random_number(digits=8),
        member_name=fake.name(),
        dependence=fake.company(),
        cost_center=fake.random_int(min=1000, max=9999),
        purchase_reason=fake.text(),
        total=fake.random_int(min=100, max=1000),
        advance_total=fake.random_int(min=50, max=500),
        employee_balance_value=fake.random_int(min=0, max=500),
        icesi_balance_value=fake.random_int(min=0, max=500),
        signature_status=fake.boolean(),
        bank=random.choice(banks),
        account_type=fake.random_element(elements=("Savings", "Checking")),
        account_number=fake.iban(),
        observations=fake.text(),
        team_id=fake.random_int(min=1, max=10),
    )
    with transaction.atomic():
        advance_legalization.id = get_next_id()
    advance_legalization.save()

    # Crear varias entradas de ejemplo para AdvanceLegalization_Table asociadas
    for _ in range(
        fake.random_int(min=1, max=5)
    ):  # Puedes ajustar el rango según tus necesidades
        advance_table = AdvanceLegalization_Table(
            general_data=advance_legalization,
            category=fake.word(),
            provider=fake.company(),
            pesos=fake.random_int(min=100, max=1000),
            concept=fake.text(),
        )
        advance_table.save()


def create_fake_billing_account():
    billing_account = BillingAccount(
        request_date=fake.date_between(start_date="-30d", end_date="today"),
        final_date=fake.date_between(start_date="today", end_date="+30d"),
        full_name=fake.name(),
        id_person=fake.random_number(digits=8),
        member_name=fake.name(),
        status=fake.random.choice(requestStatus),
        value=fake.random_int(min=100, max=1000),
        concept_reason=fake.sentence(),
        retention=fake.word(),
        tax_payer=fake.word(),
        resident=fake.word(),
        request_city=fake.city(),
        address=fake.address(),
        phone_number=fake.phone_number(),
        signature_status=fake.random_element(
            elements=("Pendiente", "Aprobada", "Rechazada")
        ),
        bank=random.choice(banks),
        account_type=fake.random_element(elements=("Savings", "Checking")),
        account_number=fake.iban(),
        cex_number=fake.random_number(digits=8),
        team_id=fake.random_int(min=1, max=10),
    )
    with transaction.atomic():
        billing_account.id = get_next_id()
    billing_account.save()


def create_fake_requisition():
    requisition = Requisition(
        request_date=fake.date_between(start_date="-30d", end_date="today"),
        final_date=fake.date_between(start_date="today", end_date="+30d"),
        requester_name=fake.name(),
        id_person=fake.random_number(digits=8),
        member_name=fake.name(),
        status=fake.random.choice(requestStatus),
        work=fake.job(),
        dependence=fake.company(),
        cenco=fake.random_int(min=1000, max=9999),
        id_value=fake.random_number(digits=8),
        description=fake.text(),
        signature_status=fake.boolean(),
        bank=random.choice(banks),
        account_type=fake.random_element(elements=("Savings", "Checking")),
        account_number=fake.iban(),
        observations=fake.text(),
        team_id=fake.random_int(min=1, max=10),
    )
    with transaction.atomic():
        requisition.id = get_next_id()
    requisition.save()


form_amount = 10
for _ in range(form_amount):
    create_fake_billing_account()
print(f"Generated {form_amount} billing accounts")
for _ in range(form_amount):
    create_fake_requisition()
print(f"Generated {form_amount} requisitions")
for _ in range(form_amount):
    create_fake_advance_legalization()
print(f"Generated {form_amount} advance legalizations")
for _ in range(form_amount):
    create_fake_travel_expense_legalization()
print(f"Generated {form_amount} travel expense legalizations")
for _ in range(form_amount):
    create_fake_travel_request()
print(f"Generated {form_amount} travel requests")
