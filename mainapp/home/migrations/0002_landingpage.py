# Generated by Django 4.0.6 on 2022-07-07 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandingPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('landing_email', models.EmailField(max_length=254, unique=True)),
                ('ref_code', models.CharField(default='', max_length=20)),
            ],
        ),
    ]
