from .forms import UserChangeForm, UserCreationForm

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from accounts.models import MyUser, Profile


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["username", "email", "is_admin", "is_verified"]
    list_filter = ["is_admin", "is_verified"]
    fieldsets = [
        (None, {"fields": ["username", "email", "password"]}),
        (
            "Permissions",
            {"fields": ["is_admin", "is_staff", "is_superuser", "is_verified"]},
        ),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ("email", "username")
    ordering = ("username",)
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "date_of_birth")
    search_fields = ("first_name", "last_name")


admin.site.register(Profile, ProfileAdmin)
