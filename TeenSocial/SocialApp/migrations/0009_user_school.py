# Generated by Django 4.2.3 on 2023-07-19 03:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SocialApp', '0008_alter_group_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='school',
            field=models.CharField(default='Greenwich High School', max_length=64),
            preserve_default=False,
        ),
    ]