# Generated by Django 4.2.3 on 2023-09-24 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialApp', '0013_rename_date_forum_created_on_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='goal_created_on',
            field=models.DateField(auto_now=True),
        ),
    ]