from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Files, Images

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields':('address', 'contact')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields':('address', 'contact')}),
    )
    list_display=['id','username','first_name','last_name','password','address','contact']

class FilesAdmin(admin.ModelAdmin):
    list_display=['id','file_name','username','file','uploaded','updated']

class ImagesAdmin(admin.ModelAdmin):
    list_display=['id','image_name','username','image','uploaded','updated']
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Files,FilesAdmin)