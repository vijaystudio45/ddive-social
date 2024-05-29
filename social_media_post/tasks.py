import random
from celery import shared_task
from .models import GeneratePost,UserAccessToken
from social_media_post.helper import generate_facebook_post, create_post_image, create_linkedin_post
from django.utils import timezone
from datetime import timedelta
import datetime
import pytz
import json
from django.db.models import Q
from .helper import *
import os




@shared_task
def publish_post(post_id):
    post = GeneratePost.objects.get(pk=post_id)
    fb_data = None
    linkedin_data = None
    print(post.channel,'=======================================channel')
    if 'Facebook' in post.channel:
        fb_token = UserAccessToken.objects.filter(user=post.user, types='Facebook', page_id=post.page_id).first()
        
        if fb_token:
            if post.image:
                image_url = post.image.url
                print(image_url,'------------------------image_url')    
            else:
                print('esleeeeeee')
                image_url = post.generated_image
            if image_url:
                fb_data = create_post_image(post.page_id, fb_token.page_access_token, post.generated_fb_post, image_url)
            else:
                fb_data_post = create_post_fb(post.page_id, fb_token.page_access_token, post.generated_fb_post)
            # fb_data = create_post_image(post.page_id, fb_token.page_access_token, post.generated_fb_post, image_url)
            if post.fb_video:
                fb_video = post.fb_video.url
                uploaded_fb_video = fb_upload_video(fb_token.page_access_token, post.page_id, post.generated_fb_post, fb_video)
                fb_video_id = uploaded_fb_video.content.decode('utf-8')  # Decode bytes to string
                fb_video_id_json = json.loads(fb_video_id) 
                if 'id' in fb_video_id_json:
                    post.fb_page_video_id = fb_video_id_json['id']
                    post.post_status = 'Live'

            if fb_data:
                fb_data_save = json.loads(fb_data.text)
                post.facebook_page_post_id = fb_data_save.get("post_id", None)
                post.post_status = 'Live'
            elif fb_data_post:
                fb_data_save = json.loads(fb_data_post.text)
                post.facebook_page_post_id = fb_data_save.get("id", None)
                post.post_status = 'Live'  # Update post status only if Facebook post was successful
            else:
                post.facebook_page_post_id = None

    if 'LinkedIn' in post.channel:
        linkedin_token = UserAccessToken.objects.filter(user=post.user, types='LinkedIn').first()
        if linkedin_token:
            if post.fb_video:  # Assuming post.video contains the video file path\
                file_size = post.fb_video.url 
                video_url = file_size.split('?')[0]
                linkedin_data2 = upload_video_to_linkedin(linkedin_token.token, post.linkedin_page_id, video_url,post.generated_linkedin_post)
                if 'id' in linkedin_data2:
                    post.linkedin_page_video_id = linkedin_data2['id']
                    post.post_status = 'Live' 
            elif post.image or post.generated_image:
                if post.image:
                    image_url = post.image.url
                else:
                    image_url = post.generated_image
                linkedin_data_image = create_media_linkedin_post(post.linkedin_page_id, linkedin_token.token, post.generated_linkedin_post, image_url)
                save_image = linkedin_data_image.json()
                if 'id' in save_image:
                    post.linkedin_page_image_id = save_image['id']
                    post.post_status = 'Live' 
            else:
                linkedin_data_new = create_linkedin_post(post.linkedin_page_id, linkedin_token.token, post.generated_linkedin_post) 
                if 'id' in linkedin_data_new:
                    post.linkedin_page_image_id = linkedin_data_new['id']
                    post.post_status = 'Live'  
                



                
    if 'Instagram' in post.channel:
        Instagram_token = UserAccessToken.objects.filter(user=post.user, types='Facebook').first()
        
        if Instagram_token:
            if post.fb_video:
                video_url = post.fb_video.url 
                acces_token = Instagram_token.token
                instagram_video_id = post_to_instagram_video(post.Instagram_page_id,acces_token, post.generated_insta_post,video_url) 
                if 'id' in instagram_video_id:
                    post.instagram_page_video_id = instagram_video_id['id']
                    post.post_status = 'Live'
               

            if post.image:
                image_url = post.image.url
            else:
                image_url = post.generated_image
            acces_token = Instagram_token.token
            instagram_Post_id = post_to_instagram_story(post.Instagram_page_id,acces_token, post.generated_insta_post, image_url)      
            if 'id' in instagram_Post_id:
                post.instagram_page_post_id = instagram_Post_id['id']
                post.post_status = 'Live'
                

    post.save()





@shared_task
def publish_scheduled_posts():
    # now = datetime.datetime.now(pytz.timezone('Asia/Kolkata')) #our time zone
    client_timezone = pytz.timezone('Europe/London')  # Assuming your client is in the UK
    now = timezone.now().astimezone(client_timezone)
    formatted_now = now.strftime('%Y-%m-%d %H:%M:%S') 
    print(formatted_now,'--------')
    scheduled_posts = GeneratePost.objects.filter(post_status='Approve',post_date__lt=formatted_now)
    # scheduled_posts = GeneratePost.objects.filter(Q(post_date__lt=now) & Q(post_status='Inprogress'))
    for post in scheduled_posts:
        publish_post.delay(post.pk)