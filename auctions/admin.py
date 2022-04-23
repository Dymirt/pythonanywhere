from django.contrib import admin
from .models import User, Category, Listing, Bid, Comment

# Register your models here
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'user', 'date')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description')
    ordering = ('is_active', 'date')


