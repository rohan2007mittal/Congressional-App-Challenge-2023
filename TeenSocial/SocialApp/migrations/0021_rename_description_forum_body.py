# Generated by Django 4.2.3 on 2023-09-27 02:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('SocialApp', '0020_alter_group_group_img'),
    ]

    operations = [
        migrations.RenameField(
            model_name='forum',
            old_name='description',
            new_name='body',
        ),
    ]