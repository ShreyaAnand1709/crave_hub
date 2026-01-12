from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('',views.index),
    path('open_signin', views.open_signin, name='open_signin'),
    path('open_signup', views.open_signup, name='open_signup'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('add_rest', views.add_rest, name="add_rest"),
    path('add_restaurant', views.add_restaurant, name="add_restaurant"),
    path('show_restaurant', views.show_restaurant, name="show_restaurant"),
    path('update_menu/<int:restaurant_id>/', views.update_menu, name="update_menu"),
    path('updating_menu/<int:restaurant_id>/', views.updating_menu, name="updating_menu"),
    path('show_restaurant_cust', views.show_restaurant_cust, name="show_restaurant_cust"),
    path('place_order/<int:restaurant_id>/', views.place_order, name="place_order"),
    path('update_restaurant_info/<int:restaurant_id>', views.update_restaurant_info, name="update_restaurant_info"),
    path('open_update_restaurant/<int:restaurant_id>', views.open_update_restaurant, name="open_update_restaurant"),
    path('delete_rest<int:restaurant_id>', views.delete_rest, name="delete_rest"),
    path('add_to_cart/<int:item_id>' , views.add_to_cart, name="add_to_cart"),
    path('admin_home', views.admin_home, name="admin_home"),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/<str:username>', views.checkout, name="checkout"),
]