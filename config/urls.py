from django.contrib import admin
from django.urls import path, include
from caka import views
from caka.auth import userlogin

urlpatterns = [
    path('admin/', admin.site.urls),

    path('base', views.BASE, name='base'),
    path('', views.HOME, name='home'),
    path('contact', views.CONTACT_US, name='contact_us'),
    path('about', views.ABOUT_US, name='about_us'),
    path('course/single', views.SINGLE_COURSE, name='single_course'),
    path('course/list', views.LIST_COURSE, name='list_course'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('doLogin', userlogin.DO_LOGIN, name='doLogin'),
    path('accounts/register', userlogin.REGISTER, name='register'),
    path('accounts/profile', userlogin.PROFILE, name='profile'),
    path('accounts/profile/update', userlogin.PROFILE_UPDATE, name='profile_update'),

    # custom pages
    path('customLogin', views.CUSTOM_LOGIN, name='customLogin'),
]
