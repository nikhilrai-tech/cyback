from django.urls import path

from .views import *

urlpatterns = [
    path('sendemail', sendemail,name='admin-sendemail'),
    # path('createbackup', createbackup,name='create-backup'),
    # path('duplicate', duplicate,name='create-duplicate'),
    path('profile', adminprofile,name='admin-profile'),
    path('profilepic', profilepic, name='profile'),
    path('settings', settings,name='admin-settings'),
    path('about', about,name='admin-about'),
]