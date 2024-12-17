from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account


@admin.register(Account)
class CustomUserAdmin(UserAdmin):
    model = Account
    list_display = ['username', 'email', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)
