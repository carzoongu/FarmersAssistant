from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('chatbot', views.chatbot, name='chatbot'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('forecast', views.forecast, name='forecast'),
]
