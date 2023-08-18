from django.contrib import admin
from user_app.models import Profile
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from django.contrib.auth.models import User


class BrandAdmin(ImportExportModelAdmin):
    pass

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name','is_valid')
    list_display_links =  ('name','is_valid')

    search_fields= ('name','is_valid',)
    list_filter= ('name','is_valid',)

class Profiles(ProfileAdmin,BrandAdmin):
    pass

admin.site.register(Profile,Profiles)


