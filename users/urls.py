"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from users.apps import UsersConfig
from users.views import (LoginApiView, ValidateApiView, ProfileApiView, ReferralApiView,
                         LogoutApiView)


app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('logout/', LogoutApiView.as_view(), name='logout'),
    path('validation/', ValidateApiView.as_view(), name='validation'),
    path('profile/<int:pk>/', ProfileApiView.as_view(), name='profile'),
    path('profile/<int:pk>/referral/', ReferralApiView.as_view(), name='profile-referral'),
]
