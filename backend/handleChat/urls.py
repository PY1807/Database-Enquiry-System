from django.contrib import admin
from django.urls import path,re_path
from django.views.generic import TemplateView
from . import views

urlpatterns=[
  # path('person/',views.PersonList.as_view()),
  path('',views.index,name="index"),
  path('person/',views.add,name="add"),
  path('log/',views.login),
  path('otp/',views.otp),
  path('otpv/',views.otpverify),
  path('newpass/',views.newpass),
  path('logout/',views.logout),
  path('newmessage/',views.newmessage),
  re_path(r'^.*$', views.index, name="index"),
] 