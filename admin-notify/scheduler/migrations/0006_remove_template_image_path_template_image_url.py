# Generated by Django 4.1.5 on 2023-01-30 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0005_template_image_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='template',
            name='image_path',
        ),
        migrations.AddField(
            model_name='template',
            name='image_url',
            field=models.TextField(blank=True, null=True, verbose_name='image_url'),
        ),
    ]
