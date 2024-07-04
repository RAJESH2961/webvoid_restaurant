from django.contrib import admin
from .models import Restaurant, RestaurantImage

class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_number', 'email', 'website_link', 'google_map_link', 'opening_hours', 'restaurant_style')
    search_fields = ('name', 'address', 'contact_number', 'email', 'restaurant_style')
    list_filter = ('restaurant_style',)
    inlines = [RestaurantImageInline]

@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'image')

# Alternatively, you can use this for non-decorator based registration:
# admin.site.register(Restaurant, RestaurantAdmin)
# admin.site.register(RestaurantImage, RestaurantImageAdmin)
