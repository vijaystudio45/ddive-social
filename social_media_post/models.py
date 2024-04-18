from django.db import models
# from django.contrib.auth.models import User
from authentication.models import CustomUser as User

# Create your models here.
OPTIONS_ON = (
    ('LinkedIn', 'LinkedIn'),
    ('Instagram', 'Instagram'),
    ('Facebook', 'Facebook')
)

class PostList(models.Model):
    title = models.CharField(max_length=100)
    post_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='images/')  # Specify the upload_to directory
    option = models.CharField(max_length=10, choices=OPTIONS_ON)  # Change 'options' to 'option'
    description = models.TextField()
    is_active = models.BooleanField(default = True)
    page_id = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.title
    



OPTIONS_ON = (
    ('LinkedIn', 'LinkedIn'),
    ('Instagram', 'Instagram'),
    ('Facebook', 'Facebook')
)


class UserAccessToken(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='user_access_token' )
    token = models.CharField(max_length=4000)
    types = models.CharField(max_length=10, choices=OPTIONS_ON)
    created_at = models.DateTimeField(auto_now_add=True)
    page_access_token =  models.CharField(max_length=4000,null=True,blank=True)
    page_id = models.CharField(max_length=4000,null=True,blank=True)




OPTIONS_ON = (
    ('LinkedIn', 'LinkedIn'),
    ('Instagram', 'Instagram'),
    ('Facebook', 'Facebook')
)
STATUS = (
    ('Approve', 'Approve'),
    ('Inprogress', 'Inprogress'),
    ('Live','Live'),
)


class GeneratePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generate_user',null=True,blank=True)
    name = models.CharField(max_length=100)
    post_date = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='images/',null=True,blank=True)  
    channel = models.CharField(max_length=10, choices=OPTIONS_ON)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    page_id = models.CharField(max_length=100, null=True, blank=True)
    linkedin_page_id =  models.CharField(max_length=100, null=True, blank=True)
    linkedin_page_video_id =  models.CharField(max_length=100, null=True, blank=True)
    linkedin_page_image_id =  models.CharField(max_length=100, null=True, blank=True)
    image_needed = models.BooleanField(default=False,null=True,blank=True)
    image_needed_prompt = models.CharField(max_length=100,null=True,blank=True)
    generated_image = models.CharField(max_length=600,null=True,blank=True)
    post_status = models.CharField(max_length=10, choices=STATUS,default='Inprogress',null=True,blank=True)
    generated_fb_post = models.TextField(null=True,blank=True)
    generated_insta_post = models.TextField(null=True,blank=True)
    generated_linkedin_post = models.TextField(null=True,blank=True)
    facebook_page_post_id = models.CharField(max_length=100, null=True, blank=True)
    instagram_page_post_id = models.CharField(max_length=100, null=True, blank=True)
    instagram_page_video_id = models.CharField(max_length=100, null=True, blank=True)
    fb_page_video_id = models.CharField(max_length=100, null=True, blank=True)
    fb_video = models.FileField(upload_to='videos/', null=True, blank=True)
    fb_page_name = models.CharField(max_length=100, null=True, blank=True)
    linkedin_page_name =  models.CharField(max_length=100, null=True, blank=True)
    Instagram_page_id =  models.CharField(max_length=100, null=True, blank=True)
    Instagram_page_name =  models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.name






