# Generated by Django 5.1.7 on 2025-03-26 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('user_name', models.CharField(max_length=32)),
                ('admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='driver',
            name='user_name',
            field=models.CharField(default=2, max_length=32),
            preserve_default=False,
        ),
    ]
