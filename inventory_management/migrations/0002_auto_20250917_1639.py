from django.db import migrations
from datetime import datetime
from django.utils.timezone import make_aware
import pytz


def create_initial_data(apps, schema_editor):
    CustomUser = apps.get_model('inventory_management', 'CustomUser')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    # Insertar Content Types si no existen
    content_types_data = [
        {"id": 1, "app_label": "admin", "model": "logentry"},
        {"id": 2, "app_label": "auth", "model": "permission"},
        {"id": 3, "app_label": "auth", "model": "group"},
        {"id": 4, "app_label": "contenttypes", "model": "contenttype"},
        {"id": 5, "app_label": "sessions", "model": "session"},
        {"id": 6, "app_label": "inventory_management", "model": "productcategory"},
        {"id": 7, "app_label": "inventory_management", "model": "customuser"},
        {"id": 8, "app_label": "inventory_management", "model": "product"},
        {"id": 9, "app_label": "inventory_management", "model": "worker"},
        {"id": 10, "app_label": "inventory_management", "model": "cart"},
        {"id": 11, "app_label": "inventory_management", "model": "cartstatus"},
        {"id": 12, "app_label": "inventory_management", "model": "chargecart"},
        {"id": 13, "app_label": "cart_status", "model": "cartstatus"},
        {"id": 14, "app_label": "inventory_management", "model": "dailypartcart"},
        {"id": 15, "app_label": "inventory_management", "model": "store"},
        {"id": 16, "app_label": "inventory_management", "model": "dailypart"},
        {"id": 17, "app_label": "inventory_management", "model": "wastagerecord"},
    ]

    for ct_data in content_types_data:
        ContentType.objects.get_or_create(id=ct_data["id"],
                                          defaults={"app_label": ct_data["app_label"], "model": ct_data["model"]})

    # Crear grupos si no existen
    admins_group, created = Group.objects.get_or_create(id=1, name='Administrators')
    managers_group, created = Group.objects.get_or_create(id=2, name='Managers')


    # Asignar permisos a cada grupo (por id)
    admins_permission_ids = list(range(1, 57))  # Permisos 1 a 56 para Administrators
    managers_permission_ids = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 37, 38, 39, 40, 45, 46, 47, 48, 49, 50,
                               51, 52, 53, 54, 55, 56]  # Permisos para Managers

    admins_permissions = Permission.objects.filter(id__in=admins_permission_ids)
    managers_permissions = Permission.objects.filter(id__in=managers_permission_ids)

    admins_group.permissions.set(admins_permissions)
    managers_group.permissions.set(managers_permissions)

    # Ahora los CustomUsers datos (igual que antes, con aware datetime)
    users_data = [
        {
            "password": "pbkdf2_sha256$1000000$HxL8nXRxqcIJQ3UwaMRPkR$gPbNL+Nk8FZ5nJIR7FkwHICB+kCxNQpeNj3ecSJs5p4=",
            "last_login": "2025-09-17T13:16:44-07:00",
            "is_superuser": True,
            "username": "admin",
            "first_name": "",
            "last_name": "",
            "email": "admin@gmail.com",
            "is_staff": True,
            "is_active": True,
            "date_joined": "2025-09-17T12:45:55-07:00",
            "deleted": None,
            "deleted_by_cascade": False,
            "id": "45af91d1-ccb9-4611-b83c-66a8ff48a7cb",
            "phone_number1": "",
            "phone_number2": None,
            "address": "",
            "is_confirmed": False
        },
        {
            "password": "pbkdf2_sha256$1000000$X050q2TdXoiTPXa6klVEv9$0V5b230ajhg4CF4g9JWFUFxx5iolqxQuspbvIo77hDY=",
            "last_login": "2025-09-17T13:27:34-07:00",
            "is_superuser": False,
            "username": "manager",
            "first_name": "Pepe",
            "last_name": "Manager",
            "email": "rafachannelbeats@gmail.com",
            "is_staff": False,
            "is_active": True,
            "date_joined": "2025-09-17T12:51:24-07:00",
            "deleted": None,
            "deleted_by_cascade": False,
            "id": "7df971d3-bb70-482b-bb89-90933a234482",
            "phone_number1": "",
            "phone_number2": None,
            "address": "",
            "is_confirmed": False
        }
    ]

    for user_data in users_data:
        if not CustomUser.objects.filter(username=user_data['username']).exists():
            user_data['last_login'] = datetime.fromisoformat(user_data['last_login'].replace("-07:00", "+00:00"))
            user_data['date_joined'] = datetime.fromisoformat(user_data['date_joined'].replace("-07:00", "+00:00"))
            user = CustomUser.objects.create(**user_data)

            if user.username == 'admin':
                user.groups.add(admins_group)
            elif user.username == 'manager':
                user.groups.add(managers_group)
            user.save()


class Migration(migrations.Migration):
    dependencies = [
        ('inventory_management', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]
