# Generated by Django 5.1.2 on 2025-01-20 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0052_alter_campaign_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='color',
            field=models.CharField(default='#000000', max_length=10),
        ),
    ]
