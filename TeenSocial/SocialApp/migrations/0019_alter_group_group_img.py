# Generated by Django 4.2.3 on 2023-09-26 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialApp', '0018_alter_forum_forum_attachment_alter_group_group_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='group_img',
            field=models.ImageField(default='group_images/blank-profile-picture.png', upload_to='group_images'),
        ),
    ]