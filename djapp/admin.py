from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from djapp.models import UserProfileInfo, User, Institute, Branch, Fee, FeePaid, Orders


class UserProfileInfoInline(admin.StackedInline):
    model = UserProfileInfo
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInfoInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class InstituteAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'email', 'logo', 'mobile']
    # search_fields = ('device_id', 'user_id')

admin.site.register(Institute, InstituteAdmin)


class BranchAdmin(admin.ModelAdmin):
    list_display = ['institute_name', 'name', 'slug', 'email', 'logo', 'mobile', 'address']

admin.site.register(Branch, BranchAdmin)


class FeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

admin.site.register(Fee, FeeAdmin)


class FeePaidAdmin(admin.ModelAdmin):
    list_display = ['user', 'paid_fee']

admin.site.register(FeePaid, FeePaidAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'amount', 'razorpay_id', 'fees_charged']

admin.site.register(Orders, OrdersAdmin)
