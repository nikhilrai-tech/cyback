from django.urls import path
from django.conf.urls import url
from django.conf.urls import include
from rest_framework.authtoken import views
from . import bviews

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),

    # By user ID
    # url(r'^profile/id/(?P<pk>\d+)/$', bviews.UserProfileView.as_view()),
    # By username


    path('',bviews.index),
    #Accounts
    path('login',bviews.login),
    path('signup',bviews.signup),
    path('user', bviews.CurrentLoggedInUser.as_view({'get': 'retrieve'}), name="current_user"),
    path('companysignup',bviews.companysignup),
    path('sendagain',bviews.sendagain),
    # path('verify',bviews.verify),
    path('forgotsend/<id>',bviews.forgotsend),
    path('forgotpassword',bviews.forgotpassword),
    # path('forgotconfirm/<token>',bviews.forgotconfirm),
    path('verify',bviews.verify2),
    path('changepassword',bviews.change),
    path('profiling',bviews.profile),
    path('dashboarding',bviews.dashing),
    path('profiling/<user>',bviews.profile),
    path('like/<user>',bviews.like),
    path('report/<user>',bviews.report),
    path('profilepic',bviews.propic), 
    path('editlinks',bviews.editlinks),
    path('staff',bviews.staffs),
    path('repusers',bviews.usersbyrep),
    path('repusers/<full>',bviews.usersbyrep),
    path('authusers',bviews.authusers),
    path('nonauthusers',bviews.nonauthusers), 
    path('contact',bviews.contact), 
    # url(r'^$', bviews.index),
    # url(r'^(?:.*)/?$', bviews.index),
]

