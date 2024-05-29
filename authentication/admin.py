from django.contrib import admin
from .models import CompanyList
from .models import CustomUser,Category,TeamMember,Prompt,Payment,SocialMediaSection,SocialMediaFile,StaticPrompts,Appointment,Voucher,VoucherUsage
# Register your models here.



class CompanyListAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'description') 

# # Register your models here.
admin.site.register(CompanyList, CompanyListAdmin)
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(TeamMember)
admin.site.register(Prompt)
admin.site.register(Payment)
admin.site.register(SocialMediaSection)
admin.site.register(SocialMediaFile)
admin.site.register(StaticPrompts)
admin.site.register(Appointment)
admin.site.register(Voucher)
admin.site.register(VoucherUsage)