from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from datetime import *

# Create your models here.

class User(AbstractUser):
    # already inherits user, password, email, etc.
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to='profile_images', default='profile_images/blank-profile.png')
    # blank=False makes it a required field
    weekly_goal = models.TextField(blank=True, default="")
    # auto_now_add is on creation, auto_now updates on new value
    goal_created_on = models.DateField(default=(date.today()-timedelta(days=10)))
    # private/public profile
    isPublic = models.BooleanField(default=True)
    activity = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Survey(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="surveys")
    mood = models.IntegerField()
    craving = models.IntegerField()
    today = models.BooleanField(default=False)
    motivation = models.IntegerField()
    log = models.TextField(blank=True, default="")
    date = models.DateField(auto_now_add=True)

class Affirmation(models.Model):
    quote = models.TextField() 
    author = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)

class Group(models.Model):
    # need to change
    CATEGORIES = (
        ('Select Category', 
        (   
            ('mindfulness', 'Motivation and Mindfulness '),
            ('mental', 'Mental Health'),
            ('substances', 'Substance Abuse'),
            ('behavioral', 'Behavioral Addiction'),
        )
        ),   
    )

    title = models.CharField(max_length=64)
    description = models.TextField()
    # leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="groups_led")
    admins = models.ManyToManyField(User, related_name="groups_led", blank=True)
    
    # to add a user to a group --> group.members.add(user)
    # to access group leader --> group.leader
    # you can get all members in a group using --> group.members.all()
    # to access all groups a user has joined --> user.groups_joined.all()
    # to access all groups a user leads --> user.groups_led.all()
    

    members = models.ManyToManyField(User, related_name="groups_joined", blank=True)
    # find way to keep stats of
        # like reddit karma
        # increment a variable every time a user creates a forum and how many forums they've commented on (not # of comments, but unique forum comments) 
    # use individual user stats to calculate
        # total days addiction free for whole group
    created_on = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=16, choices=CATEGORIES, default="other")
    group_img = models.ImageField(upload_to='group_images', default='group_images/blank-group.png')

    # def filename(self):
    #     return os.path.basename(self.file.name)
    
    def __str__(self):
        return self.title

class Forum(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="forums")
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forums_led")
    forum_attachment = models.FileField(upload_to="forum_attachments/%Y/%m/%d/", blank=True)
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=64)
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="forum_likes")

    def __str__(self):
        return f"{self.group}: {self.title}"
    
class Comment(models.Model):
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="comments")
    likes = models.ManyToManyField(User, blank=True, related_name="comment_likes")