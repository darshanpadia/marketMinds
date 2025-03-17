# create_admin.py
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketMinds.settings')
django.setup()

User = get_user_model()


email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

if email and password:
    if not User.objects.filter(email=email).exists():
        print(f"Creating superuser {email}...")
        User.objects.create_superuser(email=email, password=password)
    else:
        print(f"Superuser {email} already exists.")
