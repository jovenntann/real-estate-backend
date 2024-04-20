# Generated by Django 5.0.3 on 2024-04-20 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lead', '0018_alter_nextaction_options_messagestatus_company_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nextaction',
            options={'ordering': ['id'], 'verbose_name': 'Next Action', 'verbose_name_plural': 'Next Actions'},
        ),
        migrations.AlterModelOptions(
            name='status',
            options={'ordering': ['id'], 'verbose_name': 'Status', 'verbose_name_plural': 'Statuses'},
        ),
        migrations.AddField(
            model_name='lead',
            name='facebook_conversation_id',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]