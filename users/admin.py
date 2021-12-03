from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.forms import UserCreationForm
from users.models import User

admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    add_form = UserCreationForm
    fieldsets = (
        (None, {
            'fields': ('fullname', 'category', 'password', 'is_staff', 'is_superuser')
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide', 'extrapretty'),
            'fields': ('email', ),
        }),
    )
    ordering = 'fullname',
    list_display = 'email', 'fullname', 'is_superuser', 'category'
    list_filter = 'is_superuser', 'is_staff', 'category'
    search_fields = 'fullname', 'email'
