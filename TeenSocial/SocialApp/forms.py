from django.contrib.auth.forms import UserCreationForm
from django import forms
from.models import User, Group, Forum, Survey, Comment
from django.core.exceptions import ValidationError


# minimum word count of a field
def validate_min_word_count(value):
    words = value.split()
    if len(words) < 8:
        raise ValidationError("You must write at least 8 words.")

class CreateUserForm(UserCreationForm):
    
    # highschool = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username', 'style': 'padding: 10px;'}), label="Username")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'style': 'padding: 10px;'}), label="Password")

class WeeklyGoalForm(forms.Form):
    goal = forms.CharField(required=True, widget= forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a Goal', 'style': 'padding: 10px;'}), label="Weekly Goal")

class CreateGroupForm(forms.Form):
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Name', 'style': 'padding: 10px;'}), label="Title")
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description', 'style': 'padding: 10px;'}), label="Description", validators=[validate_min_word_count])
    category = forms.ChoiceField(required=True, choices=Group.CATEGORIES, widget=forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose Category', 'style': 'padding: 10px;'}), label="Choose Category")
    group_img = forms.ImageField(required=False, label="Group Image")

class CreateForumForm(forms.Form):
    def __init__(self, user, title, *args, **kwargs):
        super(CreateForumForm, self).__init__(*args, **kwargs)
        
        # Get the groups that the user leads
        groups_led = user.groups_led.all()
        
        # Get the groups that the user is a member of
        member_groups = user.groups_joined.all()
        
        # Combine the admin and member groups
        # all_groups = groups_led.union(member_groups, all=False)
        all_groups = (groups_led | member_groups).distinct()
        print(groups_led)
        print(member_groups)
        print(all_groups)


        # Ensure the queryset returns only one group by declaring an initial value
        if all_groups.count() > 0:
            # sets initial value to the group the link came from
            for i in range(len(all_groups)):
                if all_groups[i].title == title:
                    first_group = all_groups[i]
                    break
        else:
            first_group = None

        # Add the group choices to the ChoiceField
        self.fields['selected_group'] = forms.ModelChoiceField(
            queryset=all_groups,
            initial=first_group,
            widget=forms.Select(attrs={'class': 'form-control'}), label="Select a Group", required=True
        )

        self.fields['title'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Forum Name', 'style': 'padding: 10px;'}), label="Title")
        self.fields['body'] = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Body', 'style': 'padding: 10px;'}), label="Body", validators=[validate_min_word_count])
        self.fields['forum_atch'] = forms.FileField(required=False, label="Forum Attachment")
        # figure out comments

class Search(forms.Form):
    # keyword search
    field = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control ', 'placeholder': 'Search Groups', 'style': 'padding: 5px;'}), label="")
    
    CATEGORIES_CHOICES = (('', 'All Categories'), *Group.CATEGORIES[0][1])
    category = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control form-select ml-3 mr-3'}), choices=CATEGORIES_CHOICES, required=False, label='Category')

    def search(self):
        category = self.cleaned_data.get('category')
        groups = Group.objects.all()

        if category and category != '':
            groups = groups.filter(category=category)

        # print(self.CATEGORIES_CHOICES)


        for choice in Group.CATEGORIES[0][1]:
            if category == choice[0]:
                category = choice[1]
                break
        print(category)

        return [groups, category]

class DailySurveyForm(forms.Form):
    # figure out how to do the faces = 1-5 rating
    # How would you describe your mood today? (Angry, Anxious, Neutral, Happy, Excited)
    MOOD_CHOICES = (
        (1, "Angry"),
        (2, "Anxious"),
        (3, "Neutral"),
        (4, "Happy"),
        (5, "Excited"),
    )

    mood = forms.ChoiceField(choices=MOOD_CHOICES, required=True, label='How would you describe your mood today?')
    today = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-control', 'style': 'padding: 10px;'}), label="Have you engaged in any substance use or addictive behavior today?")
    craving = forms.IntegerField(required=True, min_value=1, max_value=10, step_size=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'padding: 10px;'}), label="On a scale of 1-10, rate the intensity of the cravings you experienced today.")
    motivation = forms.IntegerField(required=True, min_value=1, max_value=10, step_size=1, widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'padding: 10px;'}), label="On a scale of 1 to 10, how motivated are you today to overcome your addiction?")
    log = forms.CharField(required=False, widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Log', 'style': 'padding: 10px;'}), label="What is one thing you can do differently tomorrow to strengthen your commitment to recovery?")

class SettingsForm(forms.Form):
    bio = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Bio', 'style': 'padding: 10px;'}), label="Bio")
    isPublic = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input form-control', 'style': 'padding: 10px;'}), label="Private/Public")
    profile_img = forms.ImageField(required=False, label="Profile Image")

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3', 'placeholder': 'Comment', 'style': 'padding: 10px;'}), label="Comment")

class LikeForm(forms.Form):
    like = forms.BooleanField(required=False)