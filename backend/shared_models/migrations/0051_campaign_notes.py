# Generated by Django 5.1.2 on 2024-12-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared_models', '0050_feedbackscategory_view_color_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
