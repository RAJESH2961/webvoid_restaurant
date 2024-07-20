from django.contrib import admin
from .models import Restaurant, RestaurantImage, Menu,RestaurantReview, MenuReview, Complaint

class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'contact_number', 'email', 'opening_hours', 'restaurant_style')
    search_fields = ('name', 'address', 'contact_number', 'email', 'restaurant_style')
    list_filter = ('restaurant_style', 'opening_hours')
    inlines = [RestaurantImageInline]

@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'image')



@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'menu_name', 'amount', 'ingredients' , 'menu_image')
    list_filter = ('restaurant', 'ratings', 'amount' )
    search_fields = ('menu_name', 'related_menu_details', 'ingredients')

# Alternatively, you can use this for non-decorator based registration:
# admin.site.register(Restaurant, RestaurantAdmin)
# admin.site.register(RestaurantImage, RestaurantImageAdmin)



@admin.register(RestaurantReview)
class RestaurantReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'user_name', 'rating', 'created_at', 'is_approved')
    list_filter = ('restaurant', 'rating', 'is_approved')
    search_fields = ('user_name', 'review_text', 'restaurant')


@admin.register(MenuReview)
class MenuReviewAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'menu' , 'user_name', 'rating', 'created_at', 'is_approved')
    list_filter = ('restaurant', 'is_approved', 'rating')
    search_fields = ('user_name', 'review_text')



##User complaint form
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('name', 'raised_to' , 'submitted_at')
