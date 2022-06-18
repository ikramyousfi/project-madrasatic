from signal import signal
from django.contrib import admin

from users.models import *
from signaux.models import *
from reports.models import *
from announcements.models import *

# Register roles app models
#@admin.register(permissions)
#class PermissionsAdmin(admin.ModelAdmin):
 #   pass

#@admin.register(Role)
#class RoleAdmin(admin.ModelAdmin):
 #   pass

# Register users app models
# @admin.register(UserManager)
# class UserManagerAdmin(admin.ModelAdmin):
#     pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    fields = ("Type", "category")

@admin.register(Declaration)
class SignalsAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoriesAdmin(admin.ModelAdmin):
        fields = ("title", "description")


@admin.register(Announcement)
class AnnouncementsAdmin(admin.ModelAdmin):
    pass

@admin.register(Report)
class ReportsAdmin(admin.ModelAdmin):
    pass
