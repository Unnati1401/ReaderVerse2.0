# Generated by Django 3.0.3 on 2020-12-12 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schools', '0002_auto_20201208_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor', models.CharField(max_length=100)),
                ('org', models.CharField(max_length=100)),
                ('donated', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('verification', models.CharField(max_length=15)),
            ],
        ),
    ]
