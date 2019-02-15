from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from djapp.models import UserProfileInfo, User, Institute, Branch, Fee, FeePaid, Orders


class UserProfileInfoInline(admin.StackedInline):
    model = UserProfileInfo
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_editable = ('is_active',)
    inlines = (UserProfileInfoInline, )
    actions = ['delete_selected', ]

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        return qs.filter(is_active=False)

    def delete_selected(modeladmin, request, queryset):
        for usr in queryset:
            usr.is_active = False
            usr.save()

    def delete_model(modeladmin, request, queryset):
        queryset.is_active = False
        queryset.save()


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class InstituteAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'email', 'logo', 'mobile', 'is_active']
    list_editable = ('is_active',)
    actions = ['delete_selected']

    def get_queryset(self, request):
        qs = super(InstituteAdmin, self).get_queryset(request)
        return qs.filter(is_active=True)

    def delete_selected(modeladmin, request, queryset):
        for institute in queryset:
            institute.is_active = False
            institute.save()


admin.site.register(Institute, InstituteAdmin)


class BranchAdmin(admin.ModelAdmin):
    list_display = ['institute_name', 'name', 'slug', 'email', 'logo', 'mobile', 'address', 'is_active']
    list_editable = ('is_active',)
    actions = ['delete_selected']

    def get_queryset(self, request):
        qs = super(BranchAdmin, self).get_queryset(request)
        return qs.filter(is_active=True)

    def delete_selected(modeladmin, request, queryset):
        for branch in queryset:
            branch.is_active = False
            branch.save()

admin.site.register(Branch, BranchAdmin)


class FeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active']
    list_editable = ('is_active',)
    actions = ['delete_selected']

    def get_queryset(self, request):
        qs = super(FeeAdmin, self).get_queryset(request)
        return qs.filter(is_active=True)

    def delete_selected(modeladmin, request, queryset):
        for fee in queryset:
            fee.is_active = False
            fee.save()


admin.site.register(Fee, FeeAdmin)


class FeePaidAdmin(admin.ModelAdmin):
    list_display = ['user', 'paid_fee']

admin.site.register(FeePaid, FeePaidAdmin)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'amount', 'razorpay_id', 'fees_charged']

admin.site.register(Orders, OrdersAdmin)
