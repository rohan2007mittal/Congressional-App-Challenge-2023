from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", views.index, name="index"),
    path("survey/", views.survey, name="survey"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.signup, name="signup"),

    # logged in pages
    path("explore/", views.explore_groups, name="explore_groups"),
    path("new-group/", views.new_group, name="new_group"),
    path("group/<str:title>/new-forum/", views.new_forum, name="new_forum"),
    path("about/", views.about, name="about"),
    path("resources/", views.resources, name="resources"),
    path("profile/<str:user>/", views.profile, name="profile"),
    path("settings/", views.user_settings, name="user_settings"),
    path("group/<str:title>/", views.group_details, name="group_details"),
    path("group/<str:group_title>/forum/<str:forum_title>/", views.forum_details, name="forum_details"),
    path("group/<str:title>/<str:action>/", views.change_group_role, name="change_group_role"),
    path("group/<str:group_title>/forum/<str:forum_title>/like/<int:view>/", views.forum_add_like, name="forum_add_like"),
    path("group/<str:group_title>/forum/<str:forum_title>/<int:comment_id>/like/", views.comment_add_like, name="comment_add_like"),

    # forgot password links
    path("reset-password/", auth_views.PasswordResetView.as_view(template_name="forgot_password.html"), name="reset_password"),
    path("reset-password-sent/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path("reset-password-complete/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
