# Generated by Django 5.1.4 on 2024-12-24 03:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="document",
            name="name",
            field=models.CharField(default="Untitled Document", max_length=255),
        ),
        migrations.AlterField(
            model_name="document",
            name="file",
            field=models.FileField(upload_to="uploads/"),
        ),
    ]
