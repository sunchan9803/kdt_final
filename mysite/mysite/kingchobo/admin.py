from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm

class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    list_display = ['username', 'email', 'nickname', 'membership_number']

admin.site.register(CustomUser, CustomUserAdmin)