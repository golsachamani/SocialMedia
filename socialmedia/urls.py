from django.urls import path
from . import views

urlpatterns = [
    path("communities/", views.CommunityList.as_view(), name="community_list"),
    path("", views.Home.as_view(), name="home"),
    path("r/add/", views.CommunityAdd.as_view(), name="community_add"),
    path(
        "r/<str:community_slug>/delete/",
        views.CommunityDelete.as_view(),
        name="community_delete",
    ),
    path(
        "r/<str:community_slug>/update/",
        views.CommunityUpdate.as_view(),
        name="community_update",
    ),
    path(
        "r/<str:slug>/",
        views.CommunityDetail.as_view(),
        name="community_detail",
    ),
    path("r/<str:community_slug>/add/", views.PostAdd.as_view(), name="post_add"),
    path(
        "r/<str:community_slug>/join/",
        views.JoinCommunity.as_view(),
        name="community_join",
    ),
    path(
        "r/<str:community_slug>/leave/",
        views.leaveCommunity.as_view(),
        name="community_leave",
    ),
    path(
        "r/<str:community_slug>/<str:post_slug>/delete/",
        views.PostDelete.as_view(),
        name="post_delete",
    ),
    path(
        "r/<str:community_slug>/<str:post_slug>/update/",
        views.PostUpdate.as_view(),
        name="post_update",
    ),
    path(
        "r/<slug:community_slug>/<slug:post_slug>/vote/<str:vote_type>/",
        views.ToggleVote.as_view(),
        name="toggle_vote",
    ),
    path(
        "r/<str:community_slug>/<str:post_slug>/",
        views.PostDetail.as_view(),
        name="post_detail",
    ),
    path(
        "r/<str:community_slug>/<str:post_slug>/comments/add/",
        views.CommentAdd.as_view(),
        name="comment_add",
    ),
]
