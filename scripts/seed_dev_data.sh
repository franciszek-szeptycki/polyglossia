#!/bin/bash

python manage.py shell << EOF
from django.contrib.auth import get_user_model

User = get_user_model()

users = [
    ("admin", "admin@admin.com", "admin"),
    ("test", "test@test.com", "test"),
]

for username, email, password in users:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Created superuser: {username}")
    else:
        print(f"User {username} already exists")
EOF

python manage.py propagate_profiles_across_users
