from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='user-home'),
    path('portfolio/', views.portfolio, name='user-portfolio'),
]