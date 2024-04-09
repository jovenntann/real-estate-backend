# Generated by Django 5.0.3 on 2024-04-09 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0002_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='sender',
            field=models.CharField(choices=[('customer', 'Customer'), ('admin', 'Admin')], default='admin', max_length=10),
        ),
    ]