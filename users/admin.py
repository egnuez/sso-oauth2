from django.contrib import admin
from users.models import Apps, Users

# Register your models here.
class AppsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Apps, AppsAdmin)

class UsersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
admin.site.register(Users, UsersAdmin)
