# Generated by Django 5.1.2 on 2024-11-05 14:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, null=True)),
                ("description", models.TextField(null=True)),
                ("src_url", models.URLField(null=True)),
                ("dst_url", models.URLField(null=True)),
                ("upload_date", models.DateField(auto_now_add=True)),
                ("resolution", models.CharField(max_length=16, null=True)),
                ("size", models.PositiveIntegerField(null=True)),
                ("status", models.CharField(default="In progress")),
            ],
        ),
    ]