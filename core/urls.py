from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_view, name='menu'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('track/<int:order_id>/', views.order_success, name='order_success'), # Yeh track_order.html render karega
]