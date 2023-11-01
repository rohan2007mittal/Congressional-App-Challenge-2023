# Generated by Django 4.2.3 on 2023-09-25 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialApp', '0014_user_goal_created_on'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='leader',
            new_name='admins',
        ),
        migrations.AddField(
            model_name='group',
            name='group_img',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='group_images'),
        ),
    ]