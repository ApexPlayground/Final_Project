# Generated by Django 4.2.9 on 2024-04-13 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_medical_medicine"),
    ]

    operations = [
        migrations.RemoveField(model_name="medical", name="medicine",),
        migrations.AddField(
            model_name="medical",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="medical",
            name="diet",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="medical",
            name="medication",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="medical",
            name="precaution",
            field=models.TextField(blank=True, null=True),
        ),
    ]