from django.db import migrations
from django.db.models import Model


def create_categories(apps, schema_editor):
    Category: type[Model] = apps.get_model("users", "Category")

    categories = [
        {
            "id": 1,
            "name": "Attending thought session",
            "name_ar": "حضور جلسة الخاطرة",
            "value": 1,
        },
        {
            "id": 2,
            "name": "Preparing a thought",
            "name_ar": "تحضير خاطرة",
            "value": 2,
        },
        {
            "id": 3,
            "name": "Reading Quran",
            "name_ar": "قراءة القرآن",
            "value": 1,
        },
        {
            "id": 4,
            "name": "Reciting Quran",
            "name_ar": "تسميع القرآن",
            "value": 2,
        },
        {
            "id": 5,
            "name": "Inviting a new member",
            "name_ar": "دعوة عضو جديد",
            "value": 1,
        },
        {
            "id": 6,
            "name": "Attending team meeting",
            "name_ar": "حضور اجتماع الفريق",
            "value": 1,
        },
    ]

    for category in categories:
        Category.objects.update_or_create(
            id=category["id"],
            defaults={
                "name": category["name"],
                "name_ar": category["name_ar"],
                "value": category["value"],
            },
        )


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_categories, migrations.RunPython.noop),
    ]
