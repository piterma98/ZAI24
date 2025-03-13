from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

from model_utils import BaseModelAdmin
from users.models import User


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "email",
            "is_superuser",
            "is_staff",
            "groups",
            "user_permissions",
        )
        field_classes = {
            "email": forms.CharField,
            "is_superuser": forms.BooleanField,
            "is_staff": forms.BooleanField,
        }

    group = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    user_permissions = forms.ModelMultipleChoiceField(queryset=Permission.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs["autofocus"] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if hasattr(self, "save_m2m"):
                self.save_m2m()
        return user


@admin.register(User)
class CustomUserAdmin(BaseModelAdmin, UserAdmin):
    add_form = UserCreateForm
    ordering = ("email",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ()}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "created_at", "updated_at")},
        ),
    )
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
