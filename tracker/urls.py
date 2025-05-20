from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [
    path('update-location/', views.update_location, name='update_location'),
    path('map/<int:order_id>/', views.show_map, name='show_map'),
    path("get-route/<int:order_id>/", views.get_route, name="get_route"),
    path("get-csrf-token/", views.get_csrf_token, name="get_csrf_token"),
    path('delivery-choice/', views.delivery_choice, name='delivery_choice'),
    path('tracking/', views.tracking_driver, name='tracking'),
]
