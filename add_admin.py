import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "accounting_system.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.get(email="ccsa101010@gmail.com")
user.delete()
admin = User.objects.create_user(
    id="1010101010",
    username="admin",
    email="ccsa101010@gmail.com",
    password="1010101010",
    first_name="Accounting",
    last_name="Admin",
    is_superuser=True,
)
admin.save()