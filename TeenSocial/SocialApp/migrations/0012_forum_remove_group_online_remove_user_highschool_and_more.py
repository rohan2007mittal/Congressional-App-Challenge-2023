# Generated by Django 4.2.3 on 2023-09-19 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SocialApp', '0011_rename_school_user_highschool'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='forum_images')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=64)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='group',
            name='online',
        ),
        migrations.RemoveField(
            model_name='user',
            name='highschool',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profileimg',
            field=models.ImageField(default='blank-profile-picture.png', upload_to='profile_images'),
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.AddField(
            model_name='forum',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forums', to='SocialApp.group'),
        ),
        migrations.AddField(
            model_name='forum',
            name='leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forums_led', to=settings.AUTH_USER_MODEL),
        ),
    ]
