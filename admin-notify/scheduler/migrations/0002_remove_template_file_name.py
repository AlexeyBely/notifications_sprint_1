# Generated by Django 4.1.5 on 2023-01-30 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='file_name',
        ),
    ]
