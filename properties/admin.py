from django.contrib import admin
from .models import Property, PropertyImage, Favorite, NegotiationRequest


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display  = ['title', 'property_type', 'status', 'price', 'location',
                    'is_available', 'is_approved', 'created_by', 'created_at']
    list_filter   = ['property_type', 'status', 'is_available', 'is_approved']
    list_editable = ['is_approved']
    search_fields = ['title', 'location']
    inlines       = [PropertyImageInline]

    actions = ['approve_selected', 'reject_selected']

    def approve_selected(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'تم قبول {queryset.count()} عقار.')
    approve_selected.short_description = '✅ قبول العقارات المحددة'

    def reject_selected(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'تم رفض وحذف {count} عقار.')
    reject_selected.short_description = '🗑️ رفض وحذف العقارات المحددة'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'property', 'created_at']


@admin.register(NegotiationRequest)
class NegotiationAdmin(admin.ModelAdmin):
    list_display  = ['user', 'property', 'phone', 'offered_price', 'status', 'created_at']
    list_filter   = ['status']
    list_editable = ['status']
