# Generated by Django 5.0.1 on 2024-03-05 20:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="reservation",
            name="is_paid",
            field=models.BooleanField(default=False),
        ),
    ]
