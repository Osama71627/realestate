from django.contrib import admin
from .models import Property, PropertyImage, Favorite, NegotiationRequest


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'status', 'price', 'location', 'is_available', 'created_at']
    list_filter = ['property_type', 'status', 'is_available']
    search_fields = ['title', 'location']
    inlines = [PropertyImageInline]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'created_at']


@admin.register(NegotiationRequest)
class NegotiationAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'phone', 'offered_price', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']
