# Generated by Django 5.0.3 on 2024-04-18 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0015_alter_messagestatus_options_lead_message_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='status',
            name='color',
            field=models.CharField(default='default', max_length=50),
        ),
    ]
