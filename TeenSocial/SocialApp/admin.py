from django.contrib import admin
from .models import User, Group, Forum, Survey, Affirmation, Comment

# Register your models here.
admin.site.register(Forum)
admin.site.register(Comment)

# allows admin to see the date field
class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ('created_on',)

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('goal_created_on',)

class SurveyAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    
class AffirmationAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)

admin.site.register(Group,GroupAdmin)
admin.site.register(Survey,SurveyAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Affirmation,AffirmationAdmin)
