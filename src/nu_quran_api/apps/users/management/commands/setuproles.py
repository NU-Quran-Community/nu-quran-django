from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create user roles and assign permissions"

    def handle(self, *args, **kwargs) -> None:
        self.stdout.write(self.style.MIGRATE_HEADING("Setup roles:"))
        students, created = Group.objects.get_or_create(name="Student")
        supervisors, created = Group.objects.get_or_create(name="Supervisor")
        admins, created = Group.objects.get_or_create(name="Admin")

        students.permissions.add(
            Permission.objects.get(codename="view_user"),
        )
        supervisors.permissions.add(
            Permission.objects.get(codename="view_user"),
            Permission.objects.get(codename="change_user_activities"),
        )
        admins.permissions.add(
            Permission.objects.get(codename="view_user"),
            Permission.objects.get(codename="change_user"),
            Permission.objects.get(codename="delete_user"),
            Permission.objects.get(codename="add_user"),
        )
        self.stdout.write("  Roles and permissions successfully set up.")
