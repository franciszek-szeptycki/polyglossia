from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from tenants.infrastructure.models import Tenant


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_model = get_user_model()
        users = user_model.objects.all()
        for user in users:
            print(f"Analyzing user '{user}'")
            if not hasattr(user, 'tenant'):
                tenant = Tenant(user=user)
                tenant.save()
                print(f"Created tenant for user '{user}'")
            print("-" * 10)
