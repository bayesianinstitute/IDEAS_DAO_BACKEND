from django.contrib import admin
from ideasApi.models import News,Investment,Proposal,Events,Otp,Technology,About,Device
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html

class BrandAdmin(ImportExportModelAdmin):
    pass

class NewAdmin(admin.ModelAdmin):
    list_display = ('news_id','title','description','brief','timestamp','news_image','technologies')
    list_display_links =  ('news_id','title','description','brief','timestamp','news_image','technologies')

    search_fields= ('news_id','title','brief','timestamp','description','brief',)
    list_filter= ('news_id','title','description','brief','timestamp','technologies',)

class New(NewAdmin,BrandAdmin):
    pass

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('investment_id','title','description','timestamp','Investment_image','technologies')
    list_display_links =  ('investment_id','title','description','timestamp','Investment_image','technologies')

    search_fields= ('investment_id','title','timestamp','description',)
    list_filter= ('investment_id','title','description','timestamp','technologies',)

class Investments(InvestmentAdmin,BrandAdmin):
    pass

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_id','title','description','timestamp','meet_time','meet_link','event_image','technologies')
    list_display_links =  ('event_id','title','description','timestamp','meet_time','meet_link','event_image','technologies')

    search_fields= ('event_id','title','timestamp','description','meet_time','meet_link',)
    list_filter= ('event_id','title','description','timestamp','technologies','meet_time','meet_link',)

class Event(EventAdmin,BrandAdmin):
    pass

class ProposalAdmin(admin.ModelAdmin):
    list_display = ('proposal_id','title','description','timestamp','status')
    list_display_links =  ('proposal_id','title','description','timestamp','status')

    search_fields= ('proposal_id','title','description','timestamp','status',)
    list_filter= ('proposal_id','title','description','timestamp','status',)

class Proposals(ProposalAdmin,BrandAdmin):
    pass

class OtpAdmin(admin.ModelAdmin):
    list_display = ('expiry_time','otp_value')
    list_display_links =  ('expiry_time','otp_value')

    search_fields= ('expiry_time','otp_value',)
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
    list_display = ('technology_id','technology_name')
    list_display_links =  ('technology_id','technology_name')

    search_fields= ('technology_id','technology_name',)
    list_filter= ('technology_id','technology_name',)

class Technologies(TechnologyAdmin,BrandAdmin):
    pass

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id','device_model','os_version','ip_address','proxy_type')
    list_display_links =  ('device_id','device_model','os_version','ip_address','proxy_type')

    search_fields= ('device_id','device_model','os_version','ip_address','proxy_type',)
    list_filter= ('device_id','device_model','os_version','ip_address','proxy_type',)

class Devices(DeviceAdmin,BrandAdmin):
    pass



admin.site.register(News,New)
admin.site.register(Investment,Investments)
admin.site.register(Proposal,Proposals)
admin.site.register(Events,Event)
admin.site.register(Otp,Otps)

admin.site.register(Technology,Technologies)
admin.site.register(About,Abouts)
admin.site.register(Device,Devices)
