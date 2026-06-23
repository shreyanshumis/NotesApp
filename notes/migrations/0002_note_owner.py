from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def assign_existing_notes_to_local_owner(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    User = apps.get_model(app_label, model_name)
    Note = apps.get_model("notes", "Note")

    if not Note.objects.filter(owner__isnull=True).exists():
        return

    owner = (
        User.objects.filter(is_superuser=True).order_by("id").first()
        or User.objects.order_by("id").first()
    )
    if owner is None:
        owner = User.objects.create(
            username="local-journal-owner",
            email="local-journal-owner@example.local",
            is_active=False,
        )

    Note.objects.filter(owner__isnull=True).update(owner=owner)


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="note",
            name="owner",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(assign_existing_notes_to_local_owner, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="note",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notes",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
