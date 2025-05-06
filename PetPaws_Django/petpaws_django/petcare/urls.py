from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='petcare_home'),
    path('tips/add/', views.add_tip, name='add_tip'),
    path('tips/', views.view_tips, name='view_tips'),
    path('delete/<int:tip_id>/', views.delete_tip, name='delete_tip'),

    path('hospitals/add/', views.add_hospital, name='add_hospital'),
    path('hospitals/', views.view_hospitals, name='view_hospitals'),

    path('food/add/', views.add_food, name='add_food'),
    path('food/', views.view_food, name='view_food'),
    path('delete-food/<int:item_id>/', views.delete_food, name='delete_food'),
    path('food/<int:pk>/', views.view_food_detail, name='view_food'),


    path('clothes/add/', views.add_clothes, name='add_clothes'),
    path('clothes/', views.view_clothes, name='view_clothes'),
    path('cloth/<int:pk>/', views.view_cloth_detail, name='view_cloth'),
    path('clothes/delete/<int:item_id>/', views.delete_clothes, name='delete_clothes'),


    path('medicines/add/', views.add_medicine, name='add_medicine'),
    path('medicines/', views.view_medicines, name='view_medicines'),
    path('medicine/<int:pk>/', views.view_medicine_detail, name='view_medicine'),
    path('delete_medicine/<int:item_id>/', views.delete_medicine, name='delete_medicine'),


    path('accessories/add/', views.add_accessory, name='add_accessory'),
    path('accessories/', views.view_accessories, name='view_accessories'),
    path('accessory/<int:pk>/', views.view_accessory_detail, name='view_accessory'),
    path('accessories/delete/<int:item_id>/', views.delete_accessory, name='delete_accessory'),



    #  for payment 

     path('payment/', views.fake_payment, name='fake_payment'),
]
urlpatterns += [
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<str:category>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<str:item_key>/<str:action>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<str:item_key>/', views.remove_cart_item, name='remove_cart_item'),

]
