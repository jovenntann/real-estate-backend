# Generated by Django 5.0.3 on 2024-04-09 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0006_alter_message_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='email',
            field=models.EmailField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='lead',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]