from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.listing_view, name='listing'),
    path('properties/<int:pk>/', views.detail_view, name='detail'),
    path('properties/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('properties/<int:pk>/negotiate/', views.negotiate_view, name='negotiate'),
    path('favorites/', views.my_favorites, name='my_favorites'),
]
