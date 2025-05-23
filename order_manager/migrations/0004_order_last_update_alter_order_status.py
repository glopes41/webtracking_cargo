# Generated by Django 5.1.7 on 2025-03-28 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0003_alter_order_status_delete_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='last_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pendente', 'Pendente'), ('transito', 'Em Trânsito'), ('concluida', 'Concluída')], default='pendente', max_length=32),
        ),
    ]
