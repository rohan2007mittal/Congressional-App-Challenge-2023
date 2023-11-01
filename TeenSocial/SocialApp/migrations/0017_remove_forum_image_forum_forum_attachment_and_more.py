# Generated by Django 4.2.3 on 2023-09-25 00:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialApp', '0016_remove_group_admins_group_admins'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forum',
            name='image',
        ),
        migrations.AddField(
            model_name='forum',
            name='forum_attachment',
            field=models.FileField(blank=True, upload_to='forum_attachments/% Y/% m/% d/'),
        ),
        migrations.AlterField(
            model_name='group',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='groups_led', to=settings.AUTH_USER_MODEL),
        ),
    ]
