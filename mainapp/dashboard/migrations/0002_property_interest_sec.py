# Generated by Django 4.0.6 on 2022-08-15 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='interest_sec',
            field=models.BooleanField(default=False),
        ),
    ]