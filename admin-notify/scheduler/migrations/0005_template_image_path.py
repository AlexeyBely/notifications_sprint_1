# Generated by Django 4.1.5 on 2023-01-30 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_alter_template_file_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='template',
            name='image_path',
            field=models.ImageField(blank=True, null=True, upload_to='template/', verbose_name='image'),
        ),
    ]