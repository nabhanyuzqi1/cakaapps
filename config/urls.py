from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from caka import views
from caka.auth import userlogin
from django.conf import settings

urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('base', views.BASE, name='base'),
                  path('', views.HOME, name='home'),
                  path('404', views.PAGE_NOT_FOUND, name='404'),

                  path('contact', views.CONTACT_US, name='contact_us'),
                  path('about', views.ABOUT_US, name='about_us'),
                  path('courses', views.LIST_COURSE, name='list_course'),
                  path('courses/filter-data', views.filter_data,name='filter-data'),
                  path('course/<slug:slug>', views.COURSE_DETAILS, name='course_details'),
                  path('search', views.SEARCH_COURSE, name="search_course"),

                  path('accounts/', include('django.contrib.auth.urls')),

                  path('doLogin', userlogin.DO_LOGIN, name='doLogin'),
                  path('accounts/register', userlogin.REGISTER, name='register'),
                  path('accounts/profile', userlogin.PROFILE, name='profile'),
                  path('accounts/profile/update', userlogin.PROFILE_UPDATE, name='profile_update'),

                  path('checkout/<slug:slug>', views.CHECKOUT, name='checkout'),

                  path('my-course', views.MY_COURSE, name='my_course'),

                  path('verify_payment', views.VERIFY_PAYMENT, name='verify_payment'),

                  #endpoint


                  # custom pages
                  path('customLogin', views.CUSTOM_LOGIN, name='customLogin'),
                  path('webcheck', views.WEB_CHECK, name='webCheck'),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
