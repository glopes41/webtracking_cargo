# Generated by Django 5.1.7 on 2025-04-02 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0002_alter_driver_options_alter_driver_managers_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='driver',
            options={},
        ),
        migrations.AlterModelManagers(
            name='driver',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='driver',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='email',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='is_staff',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='is_superuser',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='driver',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='driver',
            name='password',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='driver',
            name='username',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]
