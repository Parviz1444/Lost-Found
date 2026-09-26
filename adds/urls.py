from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("form/", views.post_view, name="post"),
    path("posts/<slug:slug>/", views.post_detail_view, name="post_detail"),
    path("notifs/", views.notifs_view, name="notifs"),
    path("profile/", views.profile, name="profile"),
    path("users/<str:username>/", views.user_profile, name="user_profile"),
    path("posts/<slug:slug>/edit/", views.post_edit, name="post_edit"),
    path("posts/<slug:slug>/delete/", views.post_delete, name="post_delete"),
    path("posts/<slug:slug>/message/", views.message_view, name="message")
]
