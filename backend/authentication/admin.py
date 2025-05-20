from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from .models import User

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserAdminForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['role'].initial = None

@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'client')
    search_fields = ('username', 'email', 'client')
    ordering = ('username',)
    form = UserAdminForm
