# Generated by Django 5.0.6 on 2024-07-23 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0017_commentrecipe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='tip',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
