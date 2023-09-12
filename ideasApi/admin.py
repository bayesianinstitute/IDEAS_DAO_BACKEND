from django.contrib import admin
from ideasApi.models import News,Investment,Proposal,Events,Otp,Technology,About,Device,Member,Delegate
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

class BrandAdmin(ImportExportModelAdmin):
    pass

class NewAdmin(admin.ModelAdmin):
    list_display = ('id','title','brief','timestamp','image','technologies')
    list_display_links =  ('id','title','brief','timestamp','image','technologies')

    search_fields= ('id','title','brief','timestamp',)
    list_filter= ('title','timestamp','technologies',)

class New(NewAdmin,BrandAdmin):
    pass

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('id','title','timestamp','image','technologies')
    list_display_links =  ('id','title','timestamp','image','technologies')

    search_fields= ('id','title','timestamp',)
    list_filter= ('title','timestamp','technologies',)

class Investments(InvestmentAdmin,BrandAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','title','timestamp','image','technologies')
    list_display_links =  ('id','title','timestamp','image','technologies')

    search_fields= ('id','title','timestamp',)
    list_filter= ('title','timestamp','technologies',)

class Event(EventAdmin,BrandAdmin):
    pass

class ProposalAdmin(admin.ModelAdmin):
    list_display = ('id','title','timestamp','comment','status')
    list_display_links =  ('id','title','timestamp','comment','status')

    search_fields= ('id','title','timestamp','comment','status',)
    list_filter= ('title','timestamp','status',)

class Proposals(ProposalAdmin,BrandAdmin):
    pass

class OtpAdmin(admin.ModelAdmin):
    list_display = ('id','expiry_time','otp_value')
    list_display_links =  ('id','expiry_time','otp_value')

    search_fields= ('id','expiry_time','otp_value',)
    list_filter= ('expiry_time','otp_value',)

class Otps(OtpAdmin,BrandAdmin):
    pass

class AboutAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    list_display_links = ('title', 'content')

    search_fields = ('title', 'content')
    list_filter = ('title', 'content')

    def has_add_permission(self, request):
        # Check if there are any existing About objects
        existing_abouts_count = About.objects.count()

        # If there's already an About object, prevent adding more
        if existing_abouts_count > 0:
            return False
        
        # Allow adding an About object if none exist
        return True

class Abouts(AboutAdmin,BrandAdmin):
    pass

class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    list_display_links =  ('id','name')

    search_fields= ('id','name',)
    list_filter= ('name',)

class Technologies(TechnologyAdmin,BrandAdmin):
    pass

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id','member','device_model','os_version','ip_address','proxy_type')
    list_display_links =  ('id','member','device_model','os_version','ip_address','proxy_type')

    search_fields= ('id','member','device_model','os_version','ip_address','proxy_type',)
    list_filter= ('device_model','os_version','ip_address','proxy_type',)

class Devices(DeviceAdmin,BrandAdmin):
    pass

class MembersAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','join_time')
    list_display_links =  ('id','username','email','join_time')

    search_fields= ('id','username','email','device','join_time',)

class Members(MembersAdmin,BrandAdmin):
    pass

class DelegatesAdmin(admin.ModelAdmin):
    list_display = ('id','member','wallet_address','coin_amount','last_update')
    list_display_links =  ('id','member','wallet_address','coin_amount','last_update')

    search_fields= ('id','member','wallet_address','coin_amount','last_update',)

class Delegates(DelegatesAdmin,BrandAdmin):
    pass


admin.site.register(Member,Members)
admin.site.register(Delegate,Delegates)
admin.site.register(News,New)
admin.site.register(Investment,Investments)
admin.site.register(Proposal,Proposals)
admin.site.register(Events,Event)
admin.site.register(Otp,Otps)

admin.site.register(Technology,Technologies)
admin.site.register(About,Abouts)
admin.site.register(Device,Devices)
