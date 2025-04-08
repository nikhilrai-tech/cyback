from django.urls import path
# from django.conf.urls import url
# from django.conf.urls import include
from .views import *

urlpatterns = [
    path('jobs',getjobs),
    path('ajobs',getajobs),
    path('jobs/<type>/',getjobs),
    path('jobs/<type>/<location>',getjobs),

    path('programs',getprograms),
    path('aprograms',getaprograms),
    path('program/<pid>',program),
    path('aprogram/<pid>',aprogram),
    path('dprogram/<pid>',dprogram),
    path('fprograms/<type>',filteredprograms),
    path('favorite/<prog>/<type>',favorite),
    path('setbackground/<pid>',background),

    path('getreports',reportpl),
    path('reports/<pid>',reportpl), 
    # path('report',specreport),
    path('report/<rid>/',specreport),
    path('addcomment/<rid>/<type>',specreport),
    
    path('scopes',getscopes),
    path('scope/<sid>',scope),
    
    path('publicreports',publicreport),
    path('publicreport/<rid>',publicreport),
    
    path('apublicreports',apublicreport),
    path('apublicreport/<rid>/',apublicreport),  
]