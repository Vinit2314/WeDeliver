from django.contrib import admin

from .models import *

class orderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in order._meta.get_fields()]

admin.site.register(order, orderAdmin)