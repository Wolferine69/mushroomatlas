# Generated by Django 5.0.6 on 2024-07-08 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0009_alter_family_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='comment',
            name='new',
            field=models.BooleanField(default=False),
        ),
    ]
