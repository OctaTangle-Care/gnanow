from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.landing_page2, name='landing_page2'),
    
    
    path('feedback/',views.feedback,name="feedback"),
    
    path('landingpage1/', views.landing_page1, name="landing_page1"),
    path('login/', views.login, name="login"),
    path('logout_view/',views.logout_view,name="logout_view"),
    path('signup/', views.signup, name="signup"),
    path('user_form_submit/',views.user_form_submit, name="user_form_submit"),
        
   path('activate/<uidb64>/<token>/', views.activate, name='activate'),
   path('login_operation',views.login_operation,name="login_operation"),
   
   
   path('about/', views.about, name="about"),
   path('c_us/',views.c_us,name="c_us"),
   path('dashboard/',views.dashboard,name="dashboard"),
   path('profile/',views.profile,name="profile"),
   path('edit_profile/', views.edit_profile, name='edit_profile'),
   
#    path('wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
    #   path('wishlist/toggle/', views.toggle_wishlist, name='toggle_wishlist'),
 path('wishlist/toggle/<int:variant_id>/', views.toggle_wishlist, name='toggle_wishlist'),
 
 path('wishlist/toggle/dashboard/<int:variant_id>/', views.toggle_wishlist_dashboard, name='toggle_wishlist_dashboard'),
   
    path('wishlist/toggle/list/<int:variant_id>/', views.toggle_wishlist_p_list, name="toggle_wishlist_p_list"),
      path('wishlist/toggle/details/<int:variant_id>/', views.toggle_wishlist_p_details, name="toggle_wishlist_p_details"),
#    path('wishlist/add/variant/<int:variant_id>/', views.add_to_wishlist, name='add_to_wishlist'),
# path('wishlist/remove/variant/<int:variant_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),


path('wishlist/', views.wishlist_view, name='wishlist'),
path('cart/', views.view_cart, name='view_cart'),
path('cart/add/<int:variant_id>/', views.add_to_cart, name='add_to_cart'),
path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
path('cart/increase/<int:item_id>/', views.increase_cart_quantity, name='increase_cart_quantity'),




   path('add-address/', views.add_address, name='add_address'),
   path('add-address-order/', views.add_address_order, name='add_address_order'),
   
    path('my-addresses/', views.my_addresses, name='my_addresses'),
    path('edit-address/<int:address_id>/', views.edit_address, name='edit_address'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    
    path('placeorder',views.placeorder,name="placeorder"),
    path('order/create/', views.create_order, name='create_order'),



 path('payment/', views.process_payment, name='process_payment'),  # Handles payment selection
    path('payment/verify/', views.verify_payment, name='verify_payment'),  # Razorpay callback
    path('order/success/', views.order_success, name='order_success'),  # Order success page
    path('order/failed/', views.order_failed, name='order_failed'),    # Order failed page
    
    
    
    
path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),
    path('reset/invalid/', views.password_reset_invalid, name='password_reset_invalid'),
    
    
    
      path('products/', views.product_list, name='product_list'),
      path('products/<slug:slug>/', views.product_detail, name='product_detail'),
      
        path('categories/', views.categories_view, name='categories'),
      
       path('my-orders/', views.my_orders, name='my_orders'),
       
       path('order/<int:order_id>/items/', views.order_items, name='order_items'),

       
       path('order/<str:order_id>/cancel/', views.initiate_cancel_order, name='initiate_cancel_order'),
path('cancel/verify/',views.verify_cancel_otp, name='verify_cancel_otp'),

path('order/<str:order_id>/track/', views.track_order, name='track_order'),

       

]