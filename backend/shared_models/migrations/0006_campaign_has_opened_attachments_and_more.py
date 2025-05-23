# Generated by Django 5.1.2 on 2024-11-01 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0005_rename_email_client_contact_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='has_opened_attachments',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='duration_of_campaign',
            field=models.DurationField(help_text='Duration of the campaign in hours.'),
        ),
        migrations.AlterField(
            model_name='target',
            name='places_of_work',
            field=models.ManyToManyField(related_name='targets', to='shared_models.placeofwork'),
        ),
    ]
