# Generated by Django 4.1.5 on 2023-01-30 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_alter_template_file_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='file_path',
            field=models.FileField(null=True, upload_to='template/', verbose_name='file'),
        ),
    ]
