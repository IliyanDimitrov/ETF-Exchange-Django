from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('transactions/', views.transactions, name='transactions'),
    path('etf/', views.etf, name='etf'),
    path('etf/<str:id>', views.ticker, name='ticker'),
    path('etf-search/', views.etf_search, name='etf_search'),
]