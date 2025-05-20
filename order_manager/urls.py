from django.urls import path
from . import views

app_name = 'order_manager'

urlpatterns = [
    path('', views.order_list, name='orders'),
    path('register/', views.order_register, name='register'),
    path('open/', views.order_open_list, name='open'),
    path('update/status/',
         views.order_status_update, name='update'),
    path('register-verify/', views.register_verify, name='register_verify'),
    path('choice/', views.order_choiced, name='choice'),
    path('order-in-progress/', views.order_in_progress, name='order_in_progress'),
    path('search/', views.order_search, name='search'),
]
