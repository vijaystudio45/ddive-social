from django.contrib import admin
from .models import CompanyList
from .models import CustomUser,Category,TeamMember,Prompt,Payment,SocialMediaSection,SocialMediaFile,StaticPrompts,Appointment,Voucher,VoucherUsage,GenerateCategoryPrompt,GeneratePostPrompt,CaseFilePrompt,GenerateCaseFilePrompt,MediaPrompt  
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
admin.site.register(CaseFilePrompt)
admin.site.register(MediaPrompt)
# admin.site.register(GenerateCaseFilePrompt)
# admin.site.register(GeneratePostPrompt) 



class GenerateCategorypromptAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface
    # list_display = ('id', 'sample_prompt')

    # Define a readonly field for sample prompt
    readonly_fields = ('sample_prompt',)

    def sample_prompt(self, obj):
        # Return a sample prompt here, you can customize this as needed
        return "generate total 10 crisp complete prompts in 3 lines for the company category {text} for online posts with complete sentence at end and it should be 10 prompts."

admin.site.register(GenerateCategoryPrompt, GenerateCategorypromptAdmin)


class GeneratePostPromptAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface
    # list_display = ('id', 'sample_prompt')

    # Define a readonly field for sample prompt
    readonly_fields = ('sample_prompt',)

    def sample_prompt(self, obj):
        # Return a sample prompt here, you can customize this as needed
        return "Generate {channel} post of 100 words using the prompt {prompt_selected} and if available, extracting relevant information from {categories_text} if not available then give me relevant response.Use the {company_description} to promote in the post and create call to action in a subtle way.If you have url then show it in the post.Also use the keywords {categoriesdata} in your post."

admin.site.register(GeneratePostPrompt, GeneratePostPromptAdmin)


class GenerateCaseFilepromptAdmin(admin.ModelAdmin):
    # Define fields to display in the admin interface
    # list_display = ('id', 'sample_prompt')

    # Define a readonly field for sample prompt
    readonly_fields = ('sample_prompt',)

    def sample_prompt(self, obj):
        # Return a sample prompt here, you can customize this as needed
        return "Generate 10 prompts of 2 lines according to the {text} from a case file studies."

admin.site.register(GenerateCaseFilePrompt, GenerateCaseFilepromptAdmin)