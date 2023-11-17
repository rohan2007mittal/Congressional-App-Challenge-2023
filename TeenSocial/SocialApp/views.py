from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, CreateUserForm, CreateGroupForm, CreateForumForm, WeeklyGoalForm, DailySurveyForm, Search, SettingsForm, CommentForm
from .models import User, Group, Forum, Survey, Affirmation, Comment
from datetime import *
import requests
import json
from random import randrange


@login_required(login_url="login")
def index(request):
    
    form = WeeklyGoalForm()
    survey = DailySurveyForm()
    
    # only show survey if user hasn't already completed it on the current day
    # get survey streak
    surveys = request.user.surveys.all()
    temp_date = 0
    year_surveys = 0
    streak = 0
    longest_streak = 0
    for s in surveys:
        # first s in surveys
        if temp_date == 0:
            streak += 1
            temp_date = s.date
        else:    
            if s.date == temp_date + timedelta(days = 1):
                streak += 1
            else: 
                if longest_streak < streak:
                    longest_streak = streak
                streak = 1
            temp_date = s.date

        # remove survey if already completed today
        if s.date == date.today():
            survey = ""
        
            # get # of surveys completed in the current year 
        if s.date.year == date.today().year:
            year_surveys += 1

    percent_year = round(year_surveys / 365 * 100, 2)

    
    # all user progress analytics
    
    # goals to hit by completing the survey each day
    STREAK_GOALS = [3, 7, 14, 30, 60, 120, 180, 365, 548] 
    num_goals = 0
    for goal in STREAK_GOALS:
        if longest_streak >= goal:
            num_goals += 1
        else:
            next_goal = [goal, goal - streak]
            break
    
    # convert streak into array of streak value and streak percent to next goal
    streak = [streak, round(streak / next_goal[0] * 100)]


    if request.method == "POST":
        form = WeeklyGoalForm(request.POST)
        if form.is_valid():
            goal = form.cleaned_data.get("goal")    
            
            # add to user model
            user = request.user
            user.weekly_goal = goal
            user.goal_created_on = date.today()
            user.save()

            return redirect("index")
        messages.info(request, "Invalid form")
        return redirect("index")
    
    groups_joined = request.user.groups_joined.all()
    groups_led = request.user.groups_led.all()

    # get first 3 groups to show to user before div expands
    # maybe later show the 3 most active/relevant/most members/etc. groups
    cut_groups = []
    if len(groups_led) >= 3:
        cut_groups = groups_led.filter()[:3]
    elif len(groups_led) == 2:
        cut_groups = [groups_led[0], groups_led[1]]
        if len(groups_joined) > 0:
            cut_groups.append(groups_joined[0])
    elif len(groups_led) == 1:
        cut_groups = [groups_led[0]]
        if len(groups_joined) > 1:
            cut_groups.append([groups_joined[0], groups_joined[1]])
        elif len(groups_joined) == 1:
            cut_groups.append(groups_joined[0])
    else:
        for group in groups_joined:
            cut_groups.append(group)

    other_groups = []
    for group in groups_led:
        if group not in cut_groups:
            other_groups.append(group)

    for group in groups_joined:
        if group not in cut_groups:
            other_groups.append(group)

    canUpdateGoal = False

    if request.user.weekly_goal == "":
        canUpdateGoal = True
    if (date.today() - request.user.goal_created_on) > timedelta(days=7):
        canUpdateGoal = True
    
    weekly_goal = (canUpdateGoal, request.user.weekly_goal)

    # default values
    # get previous affirmation date to see if you need a new one
    affirmation = Affirmation.objects.last()
    a_date = Affirmation.objects.last().date
    
    # daily inspirational quote --> Ninjas quotes api
    if a_date + timedelta(days=1) <= date.today():
        key = "8Iaslj6xkgTwNByMj7zW0g==kGgYHTlUzoUWhzCB"
        # choose between happiness, inspirational, success
        categories = ["happiness", "inspirational", "success"]
        api_url = 'https://api.api-ninjas.com/v1/quotes?category={}'.format(categories[randrange(3)])
        response = requests.get(api_url, headers={'X-Api-Key': key})
        if response.status_code == requests.codes.ok:
            parsed = json.loads(response.text)
            affirmation = Affirmation(quote=parsed[0]["quote"], author=parsed[0]["author"])
            affirmation.save()
            quote_refresh = date.today()
        else:
            affirmation = "Opportunities don't happen, you create them."

    context = {
        "streak": streak,
        "num_goals": num_goals,
        "next_goal": next_goal,
        "percent_year": percent_year,
        "form": form,
        "survey": survey, 
        "groups_joined": groups_joined, 
        "groups_led": groups_led, 
        "cut_groups": cut_groups,
        "other_groups": other_groups,
        "affirmation": affirmation, 
        "weekly_goal": weekly_goal,
    }
    return render(request, "index.html", context)

@login_required(login_url="login")
# POST ONLY METHOD
def survey(request):
    # only handles popup survey 
    if request.method == "POST":
        # get data and add to database
        # update progress bar and other tracked goals
        form = DailySurveyForm(request.POST)
        if form.is_valid():
            mo = request.POST.get("mood")    
            c = request.POST.get("craving")    
            t = request.POST.get("today")    
            m = request.POST.get("motivation")    
            l = request.POST.get("log")

            # change format of today boolean
            if t == "yes":
                t = True
            else:
                t = False
            s = Survey(user=request.user, mood=mo, craving=c, today=t, motivation=m, log=l)
            s.save()
    return redirect("index")

def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        form = LoginForm()
        if request.method == "POST":
            
            form = LoginForm(request.POST)
            if form.is_valid():
               
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
               
                # attempt to sign user in
                user = authenticate(request, username=username, password=password)

                # Check if authentication successful
                if user is not None:
                    login(request, user)
                    return redirect("index")
                else:
                    messages.info(request, "Invalid username and/or password")
                    return redirect('login')
        context = {"form": form}
        return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect("login")

def signup(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        form = CreateUserForm()
        
        if request.method == "POST":
            
            form = CreateUserForm(request.POST)
            if form.is_valid():
               
                username = form.cleaned_data.get("username")
                email = form.cleaned_data.get("email")
                password = form.cleaned_data.get("password1")



                all_members = User.objects.all()
                all_emails = []
                for member in all_members:
                    all_emails.append(member.email.lower())

                if email.lower() in all_emails:
                    messages.info(request, f"The email: {email} is linked to an existing user")
                    return redirect("signup")
                
                form.save()


                # send signup email to user
                subject = 'Welcome to RecoverTogether'
                message = f'Hi {username}! Thank you for signing up for RecoverTogether.'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail(subject, message, email_from, recipient_list)

                # automatically logs user in
                user = authenticate(request, username=username, password=password)
                login(request, user)
                
                return redirect("index")
           
        context = {
            "form": form,
        }
        return render(request, "signup.html", context)

@login_required(login_url="login")
def explore_groups(request):
    # redirect to index to show survey if the user didn't fill it out on current day
    surveys = request.user.surveys.all()
    today = False
    for s in surveys:
        if s.date == date.today():
            today = True
    if not today:
        return redirect("index")

    # define search groups form
    form = Search()

    # get all groups aka no filters set
    all_groups = Group.objects.all()

    # top 3 trending groups -- by most members for now
    trending_num = []
    trending_name = []
    for group in all_groups:
        trending_num.append(len(group.members.all()) + len(group.admins.all()))
        trending_name.append(group.title)

    trending_combined = sorted(zip(trending_num, trending_name), reverse=True)[:3]
    # gets actual group objects for the trending groups
    trending = []
    for i in range(0,3):
        if i > len(trending_combined) - 1:
            continue
        trending.append([trending_combined[i], all_groups.filter(title=trending_name[i])[0]])

    if request.method == "POST":
        # get search groups form data
        all_group_names = []
        for group in all_groups:
                all_group_names.append(group.title)
        
        

        form = Search(request.POST)
        if form.is_valid():
            # returns [all matches for keyword and category, category name]
            form_search = form.search()
            groups = form_search[0]
            category = form_search[1]
            if category == "":
                category = "No filters"

            all_group_names = []
            for group in groups:
                all_group_names.append(group.title)

            search_results = []
            field = form.cleaned_data["field"]
            for group_name in all_group_names:
                # direct match
                if field in all_group_names:
                    # go to that group
                    return redirect("group_details", title=field)
                    
                # substring match
                if field.lower() in group_name.lower():
                    search_results.append(group_name)

            # makes sure after filtering that the group image is loaded
            
            # get group object for each search result
            search_groups = []
            for i in range(len(search_results)):
                for group in groups:
                    if search_results[i] == group.title:
                        search_groups.append(group)
            
            # for group in groups:
            #     for i in range(len(groups)):
            #         if search_results[i] == group.title:
            #             search_groups.append(group)
            
            context = {
                'groups': search_groups,
                'trending': trending,
                'category': category,
                'search': Search(),
                'title': field
            }
            return render(request, "explore_groups.html", context)
    
    # get request method
    context = {
        'groups': all_groups,
        'trending': trending,
        'category': "No filters",
        'search': Search()

    }
    return render(request, "explore_groups.html", context)

def about(request):
    if request.user.is_authenticated:
        # redirect to index to show survey if the user didn't fill it out on current day
        surveys = request.user.surveys.all()
        today = False
        for s in surveys:
            if s.date == date.today():
                today = True
        if not today:
            return redirect("index")
    return render(request, "about.html")

@login_required(login_url="login")
def resources(request):
    if request.user.is_authenticated:
        # redirect to index to show survey if the user didn't fill it out on current day
        surveys = request.user.surveys.all()
        today = False
        for s in surveys:
            if s.date == date.today():
                today = True
        if not today:
            return redirect("index")
        
    # find way to let users save resources at the top of the page 
    return render(request, "resources.html")

@login_required(login_url="login")
def profile(request, user):
# def profile(request, username):
    # redirect to index to show survey if the user didn't fill it out on current day
    surveys = request.user.surveys.all()
    today = False
    for s in surveys:
        if s.date == date.today():
            today = True
    if not today:
        return redirect("index")
    
    # mood graph data
    daily_evals = []
    
    # get all user stats
    user = User.objects.get(username=user)
    surveys = user.surveys.all()
    temp_date = 0
    streak = 0
    longest_streak = 0
    for s in surveys:
        # gets mood metric
        if s.today:
            daily_evals.append([2*s.mood + s.motivation - s.craving, s.date])
        else:
            daily_evals.append([2*s.mood + s.motivation - (s.craving-3), s.date])
        # first s in surveys
        if temp_date == 0:
            streak += 1
            temp_date = s.date
        else:    
            if s.date == temp_date + timedelta(days = 1):
                streak += 1
            else: 
                if longest_streak < streak:
                    longest_streak = streak
                streak = 1
            temp_date = s.date
    
    # get activity rank
    all_activity = []
    for u in User.objects.all():
        all_activity.append(u.activity)
    all_activity.sort(reverse=True)
    for i in range(1, len(all_activity) + 1):
        if user.activity == all_activity[i-1]:
            activity_rank = [i , user.activity]
            break

    # get improved mood % 
    # (this week's mood average / all time average ) - (average of previous mood average / all time average )
    # if there are no surveys before this week --> (this week's average / all time) - (first survey in the week / all time average)
    week_average = 0
    week_count = 0
    other_average = 0
    for i in range(len(daily_evals)):
        # if surveys this week
        if daily_evals[i][1] > (date.today() - timedelta(days=7)):
            if week_average == 0:
                first = daily_evals[i][0]
            week_count += 1
            week_average += daily_evals[i][0]
        else:
            other_average += daily_evals[i][0]

    # prevent division by 0
    daily_count = len(daily_evals)
    if len(daily_evals) == 0:
        daily_count = 1
    
    if week_count == 0:
        week_count = 1

    week_average = week_average / week_count

    if other_average != 0:
        other_average = other_average / (daily_count - week_count)

    if other_average == 0:
        percent = round(week_average/first * 100 - 100, 2)
    else:
        percent = round(week_average/other_average * 100 - 100, 2)
        if percent > 0:
            percent = "+" + str(percent)

    # get journal entries from surveys
    journals = []
    for s in surveys:
        journals.append((s.log, s.date))

    # get num_goals for badges
    STREAK_GOALS = [3, 7, 14, 30, 60, 120, 180, 365, 548] 
    num_goals = 0
    for goal in STREAK_GOALS:
        if longest_streak >= goal:
            num_goals += 1

    xValues = []
    yValues = []
    count = 1
    for i in daily_evals:
        xValues.append(count)
        count += 1
        yValues.append(i[0])

    context = {
        "streak": streak,
        "total_days": len(surveys),
        "activity_rank": activity_rank,
        "user": user,
        "num_goals": num_goals,
        "journals": journals[::-1],
        "percent": percent,
        "x": xValues,
        "y": yValues
    }
    return render(request, "profile.html", context)
    
@login_required(login_url="login")
def user_settings(request):
    # redirect to index to show survey if the user didn't fill it out on current day
    surveys = request.user.surveys.all()
    today = False
    for s in surveys:
        if s.date == date.today():
            today = True
    if not today:
        return redirect("index")
    
    form = SettingsForm()
    if request.method == "POST":
        form = SettingsForm(request.POST)
        if form.is_valid():
            profile_img = form.cleaned_data.get("profile_img")    
            bio = form.cleaned_data.get("bio")
            isPublic = form.cleaned_data.get("isPublic")
            
            # add to user model
            if request.FILES:
                file = request.FILES['profile_img']
                request.user.profile_img = file
            request.user.bio = bio
            request.user.isPublic = isPublic
            request.user.save()


            return redirect("profile", user=request.user.username)

    
    # private page only
    # user/account settings
    context = {
        "form": form,
    }
    return render(request, "settings.html", context)

@login_required(login_url="login")
def change_group_role(request, title, action):
    all_groups = Group.objects.all()
    group_object = None

    for group in all_groups:
        if title == group.title:
            group_object = group
            # Exit the loop if the group is found
            break  

    if group_object is not None:
        if action == "join":
            if request.user in group_object.admins.all() or request.user in group_object.members.all():
                messages.info(request, "You are already in this group")
            else:
                group_object.members.add(request.user)
                return redirect("group_details", title=group_object.title)
        elif action == "leave":
            if request.user in group_object.admins.all():
                messages.info("The group admin cannot leave the group")
            elif request.user not in group_object.members.all():
                messages.info(request, f"You are not in the {group_object.title} group")
            else:
                group_object.members.remove(request.user)
                return redirect("group_details", title=group_object.title)
        else:
            # later maybe add delete group functionality for admins
            return redirect("index")
        return redirect("index")
    else:
        messages.info(request, "The requested group was not found")
        return redirect("explore_groups")

@login_required(login_url="login")
def new_group(request):
    # redirect to index to show survey if the user didn't fill it out on current day
    surveys = request.user.surveys.all()
    today = False
    for s in surveys:
        if s.date == date.today():
            today = True
    if not today:
        return redirect("index")
    
    form = CreateGroupForm()
    if request.method=="POST":
        form = CreateGroupForm(request.POST, request.FILES)
        if form.is_valid():
            n = form.cleaned_data["title"]
            d = form.cleaned_data["description"]
            c = form.cleaned_data["category"]

            all_groups = Group.objects.all()
            all_group_names = []
            for group in all_groups:
                all_group_names.append(group.title)
            
            if n in all_group_names:
                messages.info(request, "Group name already exists.")
            else:
                if request.FILES:
                    myfile = request.FILES['group_img']
                    g = Group(title=n, description=d, group_img=myfile, category=c)
                else: 
                    g = Group(title=n, description=d, category=c)
                g.save()
                g.admins.add(request.user)

                # redirects to group page
                return redirect("group_details", title=g.title)
                
    context = {"form": form}
    return render(request, "new_group.html", context)

@login_required(login_url="login")
def group_details(request, title):
    # redirect to index to show survey if the user didn't fill it out on current day
    surveys = request.user.surveys.all()
    today = False
    for s in surveys:
        if s.date == date.today():
            today = True
    if not today:
        return redirect("index")
    
    all_groups = Group.objects.all()
    group_object = None

    for group in all_groups:
        if title == group.title:
            group_object = group
            break  

    if group_object is not None:
        if request.user in group_object.admins.all():
            role = "admin"
        elif request.user in group_object.members.all():
            role = "member"
        else:
            role = "none"

        # get all group stats
        # leaderboard -- top 3 with longest streak and top 3 with most activity
        mostDays = []
        mostActivity = []
        def sortingKey(elem):
            return elem[1]
        for user in group_object.members.all():
            # get survey streak
            surveys = user.surveys.all()
            temp_date = 0
            streak = 0
            for s in surveys:
                # first s in surveys
                if temp_date == 0:
                    streak += 1
                    temp_date = s.date
                else:    
                    if s.date == temp_date + timedelta(days = 1):
                        streak += 1
                    else: 
                        streak = 1
                    temp_date = s.date
            mostDays.append((user, streak))
            
            # get user activity
            mostActivity.append((user, user.activity))
        for user in group_object.admins.all():
            # get survey streak
            surveys = user.surveys.all()
            temp_date = 0
            streak = 0
            for s in surveys:
                # first s in surveys
                if temp_date == 0:
                    streak += 1
                    temp_date = s.date
                else:    
                    if s.date == temp_date + timedelta(days = 1):
                        streak += 1
                    else: 
                        streak = 1
                    temp_date = s.date
            mostDays.append((user, streak))

            # get user activity
            mostActivity.append((user, user.activity))

        mostDays.sort(key=sortingKey, reverse=True)
        mostActivity.sort(key=sortingKey, reverse=True)


        # num members, rank in all groups
        trending_num = []
        trending_name = []
        for group in all_groups:
            trending_num.append(len(group.members.all()) + len(group.admins.all()))
            trending_name.append(group.title)
        trending_combined = sorted(zip(trending_num, trending_name), reverse=True)

        for i in range(0, len(trending_combined)):
            if trending_combined[i][1] == group_object.title:
                size = [i+1, len(group_object.members.all())]
                break

        # total days free
        totalDays = 0
        for user in group_object.members.all():
            surveys = 0
            for s in user.surveys.all():
                surveys += 1
            totalDays += surveys
        for user in group_object.admins.all():
            surveys = 0
            for s in user.surveys.all():
                surveys += 1
            totalDays += surveys
        
        context = {
            "group": group_object,
            "forums": group_object.forums.all(),
            "admins": group_object.admins.all(),
            "members": group_object.members.all(),
            "mostDays": mostDays[:3],
            "mostActivity": mostActivity[:3],
            "size": size,
            "totalDays": totalDays,
            "role": role,
        }
        return render(request, "group.html", context)
    else:
        messages.info(request, "The requested group was not found")
        return redirect("explore_groups")

@login_required(login_url="login")
def new_forum(request, title):
    # redirect to index to show survey if the user didn't fill it out on current day
    surveys = request.user.surveys.all()
    today = False
    for s in surveys:
        if s.date == date.today():
            today = True
    if not today:
        return redirect("index")
    
    form = CreateForumForm(request.user, title)
    if request.method=="POST":
        form = CreateForumForm(request.user, title, request.POST, request.FILES)
        if form.is_valid():
            t = form.cleaned_data["title"]
            b = form.cleaned_data["body"]
            group = form.cleaned_data["selected_group"]

            all_forums = group.forums.all()
            all_forum_names = []
            for forum in all_forums:
                all_forum_names.append(forum.title)
            
            if t in all_forum_names:
                messages.info(request, "Forum name already exists in this group")
            else:
                if request.FILES:
                    myfile = request.FILES['forum_atch']
                    f = Forum(group=group, leader=request.user, title=t, body=b, forum_attachment=myfile)
                else: 
                    f = Forum(group=group, leader=request.user, title=t, body=b)
                f.save()

                if request.user in group.admins.all():
                    role = "admin"
                elif request.user in group.members.all():
                    role = "member"
                else:
                    role = "none"
                
                # add activity to user
                request.user.activity += 2
                request.user.save()

                # redirect to group of the forum post
                context = {
                    # forum contains all data from model -- title, body, created_on, attachment, etc.
                    "group": group,
                    "forums": group.forums.all(),
                    "admins": group.admins.all(),
                    "members": group.members.all(),
                    "role": role,
                }
                return redirect('group_details', title=group.title)
                
    context = {"form": form}
    return render(request, "new_forum.html", context)

@login_required(login_url="login")
def forum_details(request, group_title, forum_title):
    form = CommentForm()
    group = Group.objects.get(title=group_title)
    print(forum_title)
    print(group)
    forum = Forum.objects.get(title=forum_title, group=group)
    comments = Comment.objects.filter(forum=forum).order_by('-created_on')

    # only allow user to see details page if user is part of the group
    if not (request.user in group.admins.all() or request.user in group.members.all()):
        messages.info(request, "Join this group to access forum discussions")
        return redirect('group_details', title=group_title)

    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data.get("comment")      
            new_comment = Comment(body=comment, author=request.user, forum=forum)
            new_comment.save()

        # get all comments again for the forum
        comments = Comment.objects.filter(forum=forum).order_by('-created_on')

        # add to user activity
        request.user.activity += 1
        request.user.save()

        context = { 
        "forum": forum,
        "group": group,
        "form": form,
        "comments": comments,
        }
        return render(request, 'forum_details.html', context)

    context = { 
        "forum": forum,
        "group": group,
        "form": form,
        "comments": comments,
    }
    return render(request, 'forum_details.html', context)

@login_required(login_url="login")
def forum_add_like(request, group_title, forum_title, view):
    group = Group.objects.get(title=group_title)
    forum = Forum.objects.get(title=forum_title, group=group)
    
    if not (request.user in group.members.all() or request.user in group.admins.all()):
        messages.info("Join this group to access forums")
        return redirect("group_details", title=group_title)
    
    is_like = False
    for like in forum.likes.all():
        if like == request.user:
            is_like = True
            break

    # already liked --> removed, vice versa
    if is_like:
        forum.likes.remove(request.user)
    else:
        forum.likes.add(request.user)
    
    # return back to correct page
    if view == 0:
        return redirect("group_details", title=group_title)
    return redirect("forum_details", group_title=group_title, forum_title=forum_title)

@login_required(login_url="login")
def comment_add_like(request, group_title, forum_title, comment_id):
    group = Group.objects.get(title=group_title)
    forum = Forum.objects.get(title=forum_title, group=group)
    comment = Comment.objects.get(id=comment_id)

    if not (request.user in group.members.all() or request.user in group.admins.all()):
        messages.info("Join this group to access forums")
        return redirect("group_details", title=group_title)
    
    is_like = False
    for like in comment.likes.all():
        if like == request.user:
            is_like = True
            break

    # already liked --> removed, vice versa
    if is_like:
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    
    return redirect("forum_details", group_title=group_title, forum_title=forum_title)