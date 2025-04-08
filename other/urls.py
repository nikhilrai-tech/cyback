from django.urls import path
from .views import *

urlpatterns = [
    path('notifications',getnotis),
    path('markread/<nid>',markread),
    path('paybounty/<rid>',paybounty),
    path('paymenthandler/<pid>',paymenthandler),
    path('bounty/<id>',bounty), 
    path('addaccount/',funding), 
    path('checkemail',checkemail),
    path('changeemail',changeemail), 
    path('checkusername',checkusername), 
    path('changeusername',changeusername), 
]