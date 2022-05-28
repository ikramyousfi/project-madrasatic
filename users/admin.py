from signal import signal
from django.contrib import admin
from roles.models import *
from users.models import *
from signaux.models import *

# Register roles app models
@admin.register(permissions)
class PermissionsAdmin(admin.ModelAdmin):
    pass

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass

# Register users app models
# @admin.register(UserManager)
# class UserManagerAdmin(admin.ModelAdmin):
#     pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Signal)
class SignalsAdmin(admin.ModelAdmin):
    pass