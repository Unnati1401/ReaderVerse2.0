# Generated by Django 3.0.3 on 2020-12-12 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0003_donation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='donated',
            new_name='donation',
        ),
    ]
