from django.contrib import admin
from stock_keeping.models import StockReading, Shop

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'get_shop', 'is_staff')

    @admin.display(description='Shop')
    def get_shop(self, instance):
        return instance.profile.shop


class StockReadingAdmin(admin.ModelAdmin):
    list_display = ('GTIN', 'expires_at', 'scanned_at', 'shop', 'get_user')

    @admin.display(description='User')
    def get_user(self, instance):
        return instance.shop.profile.user


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(StockReading, StockReadingAdmin)
admin.site.register(Shop)
