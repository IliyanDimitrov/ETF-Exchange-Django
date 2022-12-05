from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='user-home'),
    path('profile/', views.profile, name='user-profile'),
]