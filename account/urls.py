from django.urls import path

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .views import home, register_view
from .views import profile_view


urlpatterns = [


    path(
        'login/',
        LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    path(
        'register/',
        register_view,
        name='register'
    ),

    path(
        'profile/',
        profile_view,
        name='profile'
    ),

]