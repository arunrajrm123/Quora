# Generated by Django 4.2.1 on 2023-10-30 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quora_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uuser',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='uuser',
            name='repassword',
        ),
        migrations.AlterField(
            model_name='uuser',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
