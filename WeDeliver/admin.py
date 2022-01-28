from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

admin.site.site_header  =  "WeDeliver admin"   
admin.site.site_title  =  "WeDeliver admin site"
admin.site.index_title  =  "WeDeliver Admin"

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')

class orderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in order._meta.get_fields()]
    search_fields = ('order_id','user')
    list_filter = ('payment', 'flag',)
    list_display_links = ('id', 'user',)

class contactusAdmin(admin.ModelAdmin):
    list_display = [field.name for field in contactus._meta.get_fields()]
    search_fields = ('user',)
    readonly_fields = [field.name for field in contactus._meta.get_fields()]

class profileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone_no', 'address', 'image','phone_no_verification', 'email_verification',]
    search_fields = ('user',)
    list_filter = ('phone_no_verification', 'email_verification',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(order, orderAdmin)
admin.site.register(contactus, contactusAdmin)
admin.site.register(profile, profileAdmin)