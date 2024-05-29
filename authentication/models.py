from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone





class Basemodel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    keywords = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categorie"

class CompanyList(models.Model):
    title = models.CharField(max_length=100,unique=True)
    status = models.BooleanField(default=True)
    description = models.TextField()
    # category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True,related_name='company_category')
    category = models.ManyToManyField(Category, blank=True) 
    url = models.URLField(blank=True, null=True)
    media = models.FileField(upload_to='company_media/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class TeamMember(models.Model):
    capacity = models.CharField(max_length=100,null=True,blank=True)
    company = models.ForeignKey(CompanyList, on_delete=models.CASCADE,null=True,blank=True,related_name='member_company')
    availability_start = models.DateTimeField(null=True,blank=True)
    availability_end = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return f'{self.capacity}'

class Prompt(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='prompt_category')
    text = models.TextField()

class StaticPrompts(models.Model):
    personal_development = models.TextField(null=True,blank=True)
    meeting_attended = models.TextField(null=True,blank=True)

    class Meta:
        verbose_name = "Static Prompt"




# class CompanyList(models.Model):
#     title = models.CharField(max_length=100)
#     status = models.BooleanField(default=True)
#     description = models.TextField()

#     def __str__(self):
#         return self.title
    

class CustomUser(AbstractUser):
    company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, null=True, blank=True,default=None)


class Payment(Basemodel):
    user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, blank=True,related_name='user_payment')
    is_paid = models.BooleanField(default=False)


class Appointment(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.CharField(max_length=100,null=True,blank=True)
    mobile = models.CharField(max_length=100,null=True,blank=True)
    availability_start = models.DateTimeField(null=True,blank=True)
    availability_end = models.DateTimeField(null=True,blank=True)



class SocialMediaSection(models.Model):
    description = models.TextField(null=True,blank=True)
    category = models.ManyToManyField(Category, blank=True) 
    prompts = models.ManyToManyField(Prompt, blank=True)  # Allow the prompts field to be empty
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, blank=True,related_name='user_social')
    company =models.ForeignKey(CompanyList, on_delete=models.CASCADE,null=True,blank=True,related_name='user_company_social')


class SocialMediaFile(models.Model):
    social_media_section = models.ForeignKey(SocialMediaSection,null=True,blank=True,on_delete=models.CASCADE, related_name='files')
    case_file = models.FileField(upload_to='case_studies_files/')


class Voucher(models.Model):
    code = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return self.code

class VoucherUsage(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, blank=True,related_name='user_voucher')
    is_used =  models.BooleanField(default=False)
    voucher_code = models.ForeignKey(Voucher,on_delete=models.CASCADE,null=True, blank=True,related_name='voucher_user')
    
    
    def __str__(self):
        return self.user.username

# class Basemodel(models.Model):
#     created_at = models.DateTimeField(default=timezone.now)
#     is_active = models.BooleanField(default=True)

#     class Meta:
#         abstract = True


# class Category(models.Model):
#     name = models.CharField(max_length=100,null=True,blank=True)

#     def __str__(self):
#         return self.name

# class CompanyList(models.Model):
#     title = models.CharField(max_length=100,unique=True)
#     status = models.BooleanField(default=True)
#     description = models.TextField()
#     category = models.ForeignKey(Category, on_delete=models.CASCADE,blank=True, null=True,related_name='company_category')
#     url = models.URLField(blank=True, null=True)
#     media = models.FileField(upload_to='company_media/', blank=True, null=True)

#     def __str__(self):
#         return self.title
    
# class TeamMember(models.Model):
#     capacity = models.CharField(max_length=100,null=True,blank=True)
#     company = models.ForeignKey(CompanyList, on_delete=models.CASCADE,null=True,blank=True,related_name='member_company')
#     availability_start = models.DateTimeField(null=True,blank=True)
#     availability_end = models.DateTimeField(null=True,blank=True)

#     def __str__(self):
#         return f'{self.capacity}'

# class Prompt(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='prompt_category')
#     text = models.TextField()




# # class CompanyList(models.Model):
# #     title = models.CharField(max_length=100)
# #     status = models.BooleanField(default=True)
# #     description = models.TextField()

# #     def __str__(self):
# #         return self.title
    

# class CustomUser(AbstractUser):
#     company = models.ForeignKey(CompanyList, on_delete=models.CASCADE, null=True, blank=True,default=None)


# class Payment(Basemodel):
#     user= models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, blank=True,related_name='user_payment')
#     is_paid = models.BooleanField(default=False)


# class Appointment(models.Model):
#     name = models.CharField(max_length=100,null=True,blank=True)
#     email = models.CharField(max_length=100,null=True,blank=True)
#     mobile = models.CharField(max_length=100,null=True,blank=True)
#     availability_start = models.DateTimeField(null=True,blank=True)
#     availability_end = models.DateTimeField(null=True,blank=True)



# class SocialMediaSection(models.Model):
#     description = models.TextField(null=True,blank=True)
#     # prompts = models.TextField(null=True,blank=True)
#     prompts = models.ManyToManyField(Prompt, blank=True)  # Allow the prompts field to be empty
#     keywords = models.TextField(null=True,blank=True)
#     user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True, blank=True,related_name='user_social')
#     company =models.ForeignKey(CompanyList, on_delete=models.CASCADE,null=True,blank=True,related_name='user_company_social')
