# Generated by Django 5.0.6 on 2024-07-11 16:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_options'),
        ('viewer', '0014_rename_rating_rating_hodnoceni_alter_rating_recipe'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('new', models.BooleanField(default=False)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='viewer.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments_recipe', to='accounts.profile')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
