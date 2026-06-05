from django.urls import path
from . import views

urlpatterns = [
    path('properties/',                          views.listing_view,          name='listing'),
    path('properties/create/',                   views.create_property_view,  name='create_property'),
    path('properties/admin-dashboard/',          views.admin_dashboard_view,  name='admin_dashboard'),
    path('properties/<int:pk>/',                 views.detail_view,           name='detail'),
    path('properties/<int:pk>/favorite/',        views.toggle_favorite,       name='toggle_favorite'),
    path('properties/<int:pk>/negotiate/',       views.negotiate_view,        name='negotiate'),
    path('properties/<int:pk>/approve/',         views.approve_property_view, name='approve_property'),
    path('properties/<int:pk>/reject/',          views.reject_property_view,  name='reject_property'),
    path('favorites/',                           views.my_favorites,          name='my_favorites'),
    path('my-properties/',                       views.my_properties,         name='my_properties'),
]
