# Generated by Django 4.2.3 on 2023-09-28 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SocialApp', '0021_rename_description_forum_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(default='profile_images/blank-profile.png', upload_to='profile_images'),
        ),
        migrations.AlterField(
            model_name='user',
            name='weekly_goal',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mood', models.IntegerField()),
                ('craving', models.IntegerField()),
                ('today', models.BooleanField(default=False)),
                ('motivation', models.IntegerField()),
                ('log', models.TextField(blank=True, default='')),
                ('date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
