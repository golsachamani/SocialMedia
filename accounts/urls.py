from django.urls import path
from . import views
urlpatterns = [
    path('register/',views.Register.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    path('profile/', views.Profile.as_view(), name='profile'),
    path(
    "password/",
    views.PasswordChange.as_view(),
    name="password_change"
),

    path(
        "password/done/",
        views.PasswordChangeDone.as_view(),
        name="password_change_done"
    ),

]
