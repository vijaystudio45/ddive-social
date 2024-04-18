from django.contrib import admin
from .models import CompanyList
from .models import CustomUser
# Register your models here.



class CompanyListAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'description') 

# # Register your models here.
admin.site.register(CompanyList, CompanyListAdmin)
admin.site.register(CustomUser)