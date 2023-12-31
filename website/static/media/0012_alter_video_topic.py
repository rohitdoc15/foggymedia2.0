# Generated by Django 4.1.5 on 2023-06-13 05:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("pages", "0011_petrolprice"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="topic",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="videos",
                to="pages.trendingtopic",
            ),
        ),
    ]
