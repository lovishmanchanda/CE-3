from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # General Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),

    # Pets
    path('pets/', views.pets_view, name='pets'),  # List all pets
    path('pet-profile/<str:source>/<int:pet_id>/', views.pet_profile_view, name='pet_profile'),  # View a pet in detail
    path('add-pet/', views.add_pet_view, name='add_pet'),  # Add new pet
    path('edit-pet/<int:pet_id>/', views.edit_pet_view, name='edit_pet'),  # Edit existing pet
    path('delete-pet/<int:pet_id>/', views.delete_pet_view, name='delete_pet'),  # 🔥 Delete pet (added)
    path('adopt-pet/<int:pet_id>/', views.adopt_pet_view, name='adopt_pet'),  # ❤️ Adopt pet (added)
    path('wishlist/add/<int:pet_id>/', views.add_to_wishlist_view, name='add_to_wishlist'),  # ⭐ Add to wishlist (added)
    path('wishlist/remove/<int:pet_id>/', views.remove_from_wishlist_view, name='remove_from_wishlist'),
    path('manage-pets/', views.manage_pets_view, name='manage_pets'),  # Seller/Admin managing all their pets

    # Wishlist
    path('wishlist/', views.wishlist_view, name='wishlist'),

    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

    # Admin Dashboard (for shelter or admin roles)
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('manage-users/', views.manage_users_view, name='manage_users'),
    path('delete-user/<int:user_id>/', views.delete_user_view, name='delete_user'),

    path('manageflask/', views.manageflask, name='manageflask'),
    path('flaskadd/', views.addflask, name='addflask'),
    path('flaskedit/<int:pet_id>/', views.editflask, name='editflask'),
    path('flaskdelete/<int:pet_id>/', views.deleteflask, name='deleteflask'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
