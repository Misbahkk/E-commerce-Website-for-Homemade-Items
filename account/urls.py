
from django.urls import path
from account.views import login_page,logout_user,register_page, active_email,cart,add_to_cart,remove_cart,remove_coupon,checkout,payment_success,dashboard,contactUs


urlpatterns = [
    path('login/',login_page,name='login'),
    path('logout/',logout_user,name='logout'),
    path('register/',register_page,name='register'),
    path('activate/<email_token>/',active_email,name="activate_email"),
    path('cart/',cart,name='cart'),
    path('add-to-cart/<uid>',add_to_cart,name='add_to_cart'),
    path('remove-cart/<cart_item_uid>',remove_cart,name='remove_cart'),
    path('removed-coupon/<cart_id>',remove_coupon,name="removed_coupon"),
    path('checkout/', checkout, name='checkout'),
    path('success/', payment_success, name='success'),
    path('',dashboard,name='my_account'),
    path('contactUs/',contactUs,name='contact_us'),
]
