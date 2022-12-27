from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('etf/', views.etf, name='etf'),
    path('orders/checkout/', views.checkout, name='checkout'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/update/<int:pk>/', views.update_order, name='update_order'),
    path('orders/delete/<int:pk>/', views.delete_order, name='delete_order'),
    path('etf/<str:id>', views.ticker, name='ticker'),
    path('etf-search/', views.etf_search, name='etf_search'),

]