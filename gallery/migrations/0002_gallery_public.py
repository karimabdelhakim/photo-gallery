# Generated by Django 3.0.5 on 2020-04-27 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='public',
            field=models.BooleanField(default=True),
        ),
    ]
