# Generated by Django 5.1.5 on 2025-01-15 17:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_celery_results", "0011_taskresult_periodic_task_name"),
        ("store_app", "0002_product"),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskResultAdmin",
            fields=[
                (
                    "taskresult_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_celery_results.taskresult",
                    ),
                ),
            ],
            bases=("django_celery_results.taskresult",),
        ),
        migrations.AlterField(
            model_name="product",
            name="description",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
