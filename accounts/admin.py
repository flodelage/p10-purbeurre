
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ProfileCreationForm
from .models import Profile

class ProfileAdmin(UserAdmin):
    add_form = ProfileCreationForm
    model = Profile
    list_display = ['email', 'password',]

admin.site.register(Profile, ProfileAdmin)
