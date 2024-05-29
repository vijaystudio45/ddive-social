from django.shortcuts import render
from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from authentication.models import CustomUser as User,Prompt
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
# from django.utils.encoding import force_text
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.template.loader import render_to_string
from django.http import Http404
from django.views import View
import base64
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.http import JsonResponse
from .models import PostList,UserAccessToken,GeneratePost
from pyfacebook import GraphAPI
import uuid
import os
import requests
from .helper import *
import json
from django.db.models import Q
# Create your views here.



def CreatePost(request):
    if request.method == 'GET':
        access_token = UserAccessToken.objects.filter(user=request.user,types='Facebook').first()
        if access_token:
            access_token = access_token.token
        else:
            access_token = ''
        # Construct the URL
        url = f'https://graph.facebook.com/v19.0/me/accounts'

        # Construct the query parameters
        params = {
            'access_token': access_token
        }

        # Make the GET request
        response = requests.get(url, params=params)

        # Parse the response
        if response.status_code == 200:
            data = response.json()
            accounts = data.get('data', [])
            if accounts:
                for i in accounts:
                   
                    user_token = UserAccessToken.objects.filter(user=request.user, types='Facebook', page_id=i['id']).first()
                    if user_token: 
                            new_user_token = user_token
                            new_user_token.token =  access_token
                            new_user_token.page_access_token = i['access_token']
                            new_user_token.page_id = i['id']
                            new_user_token.save()

                    else:
                        user_token = UserAccessToken.objects.create(user=request.user, types='Facebook',token= access_token.token,
                                                                    page_access_token=i['access_token'],page_id=i['id'])
                        user_token.save()
            # Pass the accounts data to the template for rendering
            return render(request, 'createpost.html', {'accounts': accounts})
    return render(request, 'createpost.html')
    
    




def ItemList(request):
    item = PostList.objects.all()
    return render(request,'list.html',{'item':item})




def update_item(request, pk):
    item = get_object_or_404(PostList, pk=pk)
    if request.method == 'POST':
        item.title = request.POST['title']
        item.post_date = request.POST['post_date']
        if 'image' in request.FILES:
            item.image = request.FILES['image']
        item.option = request.POST['option']
        item.description = request.POST['description']
        item.save()
        return redirect('list')
    return render(request, 'update.html', {'item': item})


def delete_item(request, pk):
    item = get_object_or_404(PostList, pk=pk)
    item.delete()
    return redirect('list')


###########_________________________________facebook_________________________##############################


from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from django.urls import reverse
import requests


def facebook_login(request):
    redirect_uri = request.build_absolute_uri(reverse('facebook_callback'))
    facebook_dialog_url = f"https://www.facebook.com/v11.0/dialog/oauth?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&scope=manage_pages,publish_pages,pages_manage_post"
    return redirect(facebook_dialog_url)



def facebook_callback(request):
    code = request.GET.get('code')
    redirect_uri = request.build_absolute_uri(reverse('facebook_callback'))
    access_token_url = f"https://graph.facebook.com/v11.0/oauth/access_token?client_id={settings.FACEBOOK_APP_ID}&redirect_uri={redirect_uri}&client_secret={settings.FACEBOOK_APP_SECRET}&code={code}"
    response = requests.get(access_token_url)
    data = response.json()
    access_token = data.get('access_token')
   

    if access_token:
        user_id = request.user.id 
        token_type = 'Facebook'
        try:
            user_token = UserAccessToken.objects.get(user_id=user_id, types=token_type)
            user_token.token = access_token
            user_token.save()
        except UserAccessToken.DoesNotExist:
            UserAccessToken.objects.create(user_id=user_id, token=access_token)

    return redirect('/')




def facebook_post(access_token, message, media_url):
    post_url = f"https://graph.facebook.com/v11.0/me/photos"
    params = {
        'message': message,
        'url': media_url,
        'EAAMyO3w2oHEBO3HE7b56eXRCrOaDGZAzJ80pdezaGXVNsQnzFOQIaWA8DZC1uYBAxmW47ShVhZB1kuQrlD2U3ZBgpXwDiEqP74dK3dZBJy60bPZB2IADhuEB5ZAzCtcajEdeMfCAokEg67dbCPZA0QC3Jsw1ZCEAsvSGpLotpHw7KFPWj20FK0JHleHq0dPPbyVWSIzMi79ttzVigeaZBTZBVOiEWwg6GO8wBUzzu1DS8PZBBgrFCUut08wAlgaHEi26': access_token
    }
    response = requests.post(post_url, data=params)
    return response.json()



def post_on_facebook_with_media(request):
    access_token = request.session.get('access_token') 
    message = "Check out this amazing photo!"
    media_url = "https://example.com/path/to/your/image.jpg"  
    
    if access_token:
        response = facebook_post(access_token, message, media_url)
        if 'id' in response:
            return redirect('/')  
        else:
            return redirect('/')
    else:
        return redirect('/')





#####_________________________Linked In __________________________________#####################
    

from django.shortcuts import render
from django.http import JsonResponse
import requests

def generate_token(request):
    authorization_url = 'https://www.linkedin.com/oauth/v2/authorization'
    client_id = '77x0dj98nkfbjx'
    redirect_uri = 'https://ddivesocial.com/'
    state = '12345'
    scope = 'r_liteprofile'

    redirect_url = f"{authorization_url}?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}&scope={scope}"
    return redirect(redirect_url)

def get_access_token(request):
    if request.method == 'GET':
        code = request.GET.get('code')
        if code:
            url = 'https://www.linkedin.com/oauth/v2/accessToken'
            params = {
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': 'https://ddivesocial.com/linkedin/callback/access/',
                'client_id': '77x0dj98nkfbjx',
                'client_secret': 'RXh9auhH88gPQLwp'
            }
            response = requests.post(url, data=params)
            if response.status_code == 200:
                access_token = response.json()['access_token']
                return JsonResponse({'access_token': access_token})
            else:
                return JsonResponse({'error': 'Failed to retrieve access token'}, status=400)

def verify_token(request):
    if request.method == 'GET':
        access_token = request.GET.get('access_token')
        if access_token:
            api_url = 'https://api.linkedin.com/v2/me'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/json',
            }
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                return JsonResponse({'message': 'Access token is valid!'})
            else:
                return JsonResponse({'error': 'Access token is invalid or has expired'}, status=400)

def create_post(request):
    if request.method == 'POST':
        access_token = request.POST.get('access_token')
        if access_token:
            api_url = 'https://api.linkedin.com/v2/ugcPosts'
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Connection': 'Keep-Alive',
                'Content-Type': 'application/json',
            }
            post_body = request.POST.get('post_body', {})
            response = requests.post(api_url, headers=headers, json=post_body)
            if response.status_code == 201:
                return JsonResponse({'message': 'Post successfully created!'})
            else:
                return JsonResponse({'error': f'Post creation failed with status code {response.status_code}: {response.text}'}, status=400)
            



# -------------------------#generate_post_with_ai#-----------------------
            


# url = f"https://graph.facebook.com/v19.0/me/accounts"
#     params = {
#         'fields': 'id,name,access_token,instagram_business_account',
#         'access_token': access_token
#     }

#     response = requests.get(url, params=params)
#     response.raise_for_status()  
#     data = response.json()
#     print("3333333333333333333333333",data)



def GenerateAIPost(request):

    if request.method == 'GET':
        access_token_facebook = UserAccessToken.objects.filter(user=request.user, types='Facebook').first()
        if access_token_facebook:
            token_facebook = access_token_facebook.token
        else:
            token_facebook = ''
            
        access_token_linkedin = UserAccessToken.objects.filter(user=request.user, types='LinkedIn').first()
        if access_token_linkedin:
            token_linkedin = access_token_linkedin.token
            linkedin_pages = get_linkedin_pages(token_linkedin)  # Assuming get_linkedin_pages is implemented
        else:
            token_linkedin = ''
            linkedin_pages = []
        accounts_facebook = []  
        instagram_accounts = []  
        url_facebook = f'https://graph.facebook.com/v19.0/me/accounts'
        params_facebook = {
            'access_token': token_facebook,
            'fields': 'id,name,access_token,instagram_business_account'
            }
        response_facebook = requests.get(url_facebook, params=params_facebook)
        if response_facebook.status_code == 200:
            data_facebook = response_facebook.json()
            accounts_facebook = data_facebook.get('data', [])
            if accounts_facebook:
                for i in accounts_facebook:

                    user_token = UserAccessToken.objects.filter(user=request.user, types='Facebook',
                                                                page_id=i['id']).first()
                    if user_token:
                        new_user_token = user_token
                        new_user_token.token = access_token_facebook.token
                        new_user_token.page_access_token = i['access_token']
                        new_user_token.page_id = i['id']
                        new_user_token.save()

                    else:
                        print('no iddddddd')
                        # for i in accounts:
                        user_token = UserAccessToken.objects.create(user=request.user, types='Facebook',
                                                                    token=access_token_facebook.token,
                                                                    page_access_token=i['access_token'],
                                                                    page_id=i['id'])
                        user_token.save()



            instagram_accounts = [{'id': instagram['instagram_business_account']['id'], 'name': instagram['name']} for instagram in accounts_facebook if 'instagram_business_account' in instagram and 'id' in instagram['instagram_business_account'] and 'name' in instagram]
        else:
            print("ff")
        if token_linkedin:
            linkedin_pages = get_linkedin_pages(token_linkedin)  # Assuming get_linkedin_pages is implemented
        else:
            print("f")

        return render(request, 'generatepost.html', {'accounts': accounts_facebook, 'linkedin_pages': linkedin_pages,'instagram_accounts':instagram_accounts})
    
    

    if request.method == 'POST':
        name = request.POST.get('name')
        post_date = request.POST.get('post_date')
        image = request.FILES.get('image')
        print(image,'==========imageimageimage')
        channel = request.POST.getlist('option')
        print(channel,'channelchannel')
        description = request.POST.get('description')
        page_id = request.POST.get('page_id')
        # prompts = request.POST.get('prompts')
        selected_prompts = request.POST.getlist('prompts')
        selected_promptid = request.POST.get('promptId')
        # selected_prompts=[]
        # for prompt in prompts:
        #     selected_prompts.append(prompt)
        print(selected_promptid,'==================================================selected_promptid')
        print(selected_prompts,'-=-=-=-=-=selected_prompts')
        categoriesdata = request.POST.get('categoriesdata')
        print(request.POST,'posststttttttt')
        account_name = ""
        if page_id:
            page_id, account_name = page_id.split(',')
        linkedin_page_id = request.POST.get('linkedin_page_id')
     
        linkedin_name = ""
        if linkedin_page_id:
            linkedin_page_id, linkedin_name = linkedin_page_id.split(',')
        
        instagram_page_id = request.POST.get('instagram_page_id')
        Instagram_page_name = ""
        if instagram_page_id:

            instagram_page_id, Instagram_page_name = instagram_page_id.split(',')

        image_needed = request.POST.get('image_needed')
        image_prompt = request.POST.get('image_prompt')
        media_file = request.FILES.get('fb_media')
        uploaded_image = None
        fb_video = None

        if media_file:
            if 'image' in media_file.content_type:
                uploaded_image = media_file
            elif 'video' in media_file.content_type:
                fb_video = media_file
       
    

        
        if image_needed and image_prompt:
            generated_image = generate_images(image_prompt)
            uploaded_image = process_image_and_save_to_model(generated_image)
        

        data1 = None
        data2 = None
        data3 = None
        fb_data=None
        new_post = GeneratePost(
            user=request.user, name=name,
            post_date=post_date,
            image=uploaded_image,
            # generated_image='',
            channel=channel,
            fb_video=fb_video,
            description=description,
            page_id=page_id,
            fb_page_name = account_name,
            linkedin_page_name = linkedin_name,
            linkedin_page_id=linkedin_page_id,
            Instagram_page_id=instagram_page_id,
            Instagram_page_name=Instagram_page_name,
            image_needed=image_needed,image_needed_prompt=image_prompt)
        new_post.save()

        prompt_text = None

        if selected_promptid:
            prompt_text = Prompt.objects.get(id=selected_promptid).category.text
            print(prompt_text,'----------------------------------------------')
        # print(1+'1')
        selected_prompts_str = ' '.join(selected_prompts)

        if description is None:
            description = selected_prompts_str
            print(description,'][][]description')
        elif selected_prompts:
            description = selected_prompts_str + "" + description
            print(description,'========description')

        # print(1+'1')

        # print()
        
        for i in channel:
            if i == 'Facebook':
                user = request.user
                if user.company:
                    # selected_prompt = selected_prompts
                    # print(selected_prompt)
                    categoriesdata = categoriesdata
                    print(categoriesdata)
                    # additional_description= description
                    social_media_section = user.company.user_company_social.first()

                    company_description = social_media_section.description
                    print(company_description,'company_description')
                    # if selected_prompt:
                    #     description=selected_prompt
                data1 = generate_facebook_post(description,company_description,categoriesdata,prompt_text, i)
                print(data1,'ppppppppppppppppppppp')
                fb_token = UserAccessToken.objects.filter(user=request.user, types='Facebook', page_id=page_id).first()
                if fb_token:
                    # data = create_facebook_page_post(page_id,fb_token.page_access_token,description)
                    # image_upload = create_facebook_image_post(page_id,fb_token.page_access_token,item.image)
                    if new_post.image:
                        image = new_post.image.url
                    else:
                        image = new_post.generated_image

            if i == 'LinkedIn':
                user = request.user
                if user.company:
                    # selected_prompt = selected_prompts
                    # print(selected_prompt)
                    categoriesdata = categoriesdata
                    print(categoriesdata)
                    # additional_description= description
                    social_media_section = user.company.user_company_social.first()

                    company_description = social_media_section.description
                    print(company_description,'company_description')
                    # if selected_prompt:
                    #     description=selected_prompt
                token = UserAccessToken.objects.filter(user=request.user,types='LinkedIn').first()
                data2 = generate_facebook_post(description,company_description,categoriesdata,prompt_text, i)
                if token :
                    # data = create_linkedin_post(linkedin_page_id,token.token,data2)
                    print("ddd")
                if token and (new_post.image or new_post.generated_image):
                    if new_post.image:
                        image = new_post.image
                    else:
                        image = new_post.generated_image
                    # linkedin_data =  create_media_linkedin_post(linkedin_page_id,token.token,data2,f'{new_post.image.url}')

            if i == 'Instagram':
                user = request.user
                if user.company:
                    # selected_prompt = selected_prompts
                    # print(selected_prompt)
                    categoriesdata = categoriesdata
                    print(categoriesdata)
                    # additional_description= description
                    social_media_section = user.company.user_company_social.first()

                    company_description = social_media_section.description
                    print(company_description,'company_description')
                    # if selected_prompt:
                    #     description=selected_prompt
                token = UserAccessToken.objects.filter(user=request.user,types='Instagram').first()
                data3 = generate_facebook_post(description,company_description,categoriesdata,prompt_text, i)
       
        new_post.generated_fb_post = data1
        new_post.generated_insta_post = data3
        new_post.generated_linkedin_post = data2
        new_post.save()
        messages.success(request, 'Post created successfully.')
        return redirect('generated-list')  # Redirect to a success page after posting
    else:
        return render(request, 'generatepost.html')







def GeneratedItemList(request):
    user_company = request.user.company
    print(user_company,'user_company')
    item = GeneratePost.objects.filter(
    Q(post_status='Inprogress') | Q(post_status='Approve'),
    user__company=user_company
).order_by('-post_date')
    
    return render(request, 'generatedlist.html', {'item': item})




def GeneratedLiveList(request):
    user_company = request.user.company
    print(user_company, 'user_company')
    # Filter records where post_status is 'Live'
    item = GeneratePost.objects.filter(user__company=user_company, post_status='Live').order_by('-post_date')
    return render(request, 'generatedLive.html', {'item': item})



from django.core.files.uploadedfile import InMemoryUploadedFile


def UpdateGeneratedItem(request, pk):
    item = get_object_or_404(GeneratePost, pk=pk)
    if request.method == 'POST':
        item.name = request.POST.get('name', item.name)
        item.post_date = request.POST.get('post_date', item.post_date)
        item.description = request.POST.get('description', item.description)
        item.option = request.POST.getlist('option')
        item.page_id = request.POST.get('page_id', item.page_id)
        item.image_needed = request.POST.get('image_needed', False)
        item.post_status = request.POST.get('post_status')
        item.image_needed_prompt = request.POST.get('image_needed_prompt', item.image_needed_prompt)
        item.generated_fb_post = request.POST.get('generated_fb_post', item.generated_fb_post)
        item.generated_insta_post = request.POST.get('generated_insta_post', item.generated_insta_post)
        item.generated_linkedin_post = request.POST.get('generated_linkedin_post', item.generated_linkedin_post)
      
        media_file = request.FILES.get('media', None)
        if media_file:
            content_type = media_file.content_type
            if 'image' in content_type:
                item.generated_image = None  
                item.fb_video = None  
                item.image = media_file
            elif 'video' in content_type or media_file.name.lower().endswith('.mp4'):
                item.image = None 
                item.generated_image = None  
                item.fb_video = media_file

        item.save()
        return redirect('generated-list')
    return render(request, 'generatedpostupdate.html', {'item': item})


def GeneratedPostDelete(request, pk):
    item = get_object_or_404(GeneratePost, pk=pk)
    item.delete()
    return redirect('generated-list')



#to get postview
def PostView(request, pk):
    item = get_object_or_404(GeneratePost, pk=pk)
    return render(request, 'generatepostview.html', {'item': item})



#to get likes and comment in fb





# def get_facebook_like(request,id):
#     post = get_object_or_404(GeneratePost, id=id)
#     fb_token = UserAccessToken.objects.filter(user=post.user,page_id = post.page_id).first()
#     print("rrrrrrrrrrrrrrrrrrrrrrr",fb_token)
#     data_count = facebook_likes_comments(post.facebook_page_post_id,fb_token.page_access_token)
#     share_count = get_shared_count(post.facebook_page_post_id,fb_token.page_access_token)
#     if data_count is None:
#         # Handle the case where data_count is None
#         return JsonResponse({'error': 'Failed to fetch likes and comments data'})
#     likes_count = data_count['likes']['summary']['total_count']
#     comments_count = data_count['comments']['summary']['total_count']
#     response_data = {
#         'likes_count': likes_count,
#         'comments_count': comments_count,
#         'share_count':share_count
#     }
    
#     return JsonResponse(response_data, safe=False)





def get_facebook_like(request, id):
    post = get_object_or_404(GeneratePost, id=id)
    fb_token = UserAccessToken.objects.filter(user=post.user, page_id=post.page_id).first()

    if post.facebook_page_post_id:
        media_id = post.facebook_page_post_id
    elif post.fb_page_video_id:
        media_id = post.fb_page_video_id
    else:
        # Handle the case where neither instagram_page_post_id nor instagram_page_video_id exists
        return JsonResponse({'error': 'No Instagram media ID found for the post'})
    
    data_count = facebook_likes_comments(media_id, fb_token.page_access_token)
    share_count = get_shared_count(media_id, fb_token.page_access_token)
    if data_count is None:
        return JsonResponse({'error': 'Failed to fetch likes and comments data'})
    likes_count = data_count['likes']['summary']['total_count']
    comments_count = data_count['comments']['summary']['total_count']
    response_data = {
        'likes_count': likes_count,
        'comments_count': comments_count,
        'share_count': share_count
    }
    
    return JsonResponse(response_data, safe=False)


    





####-----------------------__SHIVAM--------------__####################


from django.http import JsonResponse
from .models import GeneratePost

def generate_post_list(request):
    posts = GeneratePost.objects.all()
    events = []
    for post in posts:
        event = {
            'id': post.id,
            'event_date':post.post_date.strftime("%Y-%m-%d %H:%M:%S"),  # Format the date as needed
            'event_title': post.name,
            'event_descriptions': post.description,
            'event_channel':post.channel,
            'event_status':post.post_status,
            'event_image': post.image.url if post.image else '',  # Assuming image is stored as URL
        }
        events.append(event)

    data = {'events': events}
    return JsonResponse(data, safe=False)



# ----------------------------------------------------start_get_linkedin_page---------------------------------------------


def get_linkedin_pages(access_token):
    # LinkedIn API endpoint for retrieving user's company pages
    url = 'https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee&role=ADMINISTRATOR'

    # Construct the headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
    }
    # Make the GET request to LinkedIn API
    response = requests.get(url, headers=headers)

    # Parse the response
    if response.status_code == 200:
        data = response.json()
        pages = data.get('elements', [])
        page_info = []
        for page in pages:
            page_name = get_page_name(access_token, page.get('organizationalTarget', ''))
            page_id = page.get('organizationalTarget', '').split(':')[-1]
            page_info.append({'name': page_name, 'id': page_id})

        return page_info
        # Extract page information
        # pages = data.get('elements', [])
        # return pages
    else:
        # Handle error cases, such as LinkedIn API being down or access token issues
        return None
    



def get_page_name(access_token, page_urn):
    # LinkedIn API endpoint for retrieving page details
    url = f'https://api.linkedin.com/v2/organizations/{page_urn.split(":")[-1]}'

    # Construct the headers with the access token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Connection': 'Keep-Alive',
    }

    # Make the GET request to LinkedIn API
    response = requests.get(url, headers=headers)

    # Parse the response
    if response.status_code == 200:
        data = response.json()
        page_name = data.get('localizedName', '')
        return page_name
    else:
        return None






# ===================testinggetlinkindlike comment----------------
    


def get_page_posts(token, page_id):
    headers = {
        'Authorization': 'Bearer ' + token,
        'Connection': 'Keep-Alive',
    }
    url = f'https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:{page_id}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("rrrffffffffffffffffff", data.get('elements', []))
        return data.get('elements', [])
    else:
        print("Error fetching page posts:", response.text)
        return None

def get_post_engagement(token, post_id):
    headers = {
        'Authorization': 'Bearer ' + token,
        'Connection': 'Keep-Alive',
    }
    url = f'https://api.linkedin.com/v2/shares/{post_id}/organizationalEntityShareStatistics'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # Extract engagement data for the post
        engagement_data = data.get('totalShareStatistics', {})
        return engagement_data
    else:
        print("Error fetching post engagement data:", response.text)
        return None

def GenerateAILinkedInPost(request):
    if request.method == 'GET':
        access_token = UserAccessToken.objects.filter(user=request.user, types='LinkedIn').first()
        if access_token:
            token = access_token.token
            linkedin_pages = get_linkedin_pages(token)
            page_engagement_data = []
            for page in linkedin_pages:
                page_id = page['id']
                page_name = page['name']
                posts = get_page_posts(token, page_id)
                post_engagement_data = []
                for post in posts:
                    post_id = post['id']
                    engagement = get_post_engagement(token, post_id)
                    post_engagement_data.append({
                        'post_id': post_id,
                        'engagement': engagement
                    })
                page_engagement_data.append({
                    'name': page_name,
                    'id': page_id,
                    'posts': post_engagement_data
                })
            return render(request, 'generatepost.html', {'linkedin_pages': page_engagement_data})
        else:
            return render(request, 'generatepost.html')






# def get_page_engagement(token, page_id):
#     page_id = 77015671
#     headers = {
#         'Authorization': 'Bearer ' + token,
#         'Connection': 'Keep-Alive',
#     }
#     url = f'https://api.linkedin.com/v2/organizationalEntityShareStatistics?q=organizationalEntity&organizationalEntity=urn:li:organization:{page_id}'
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         print(data,'qaqaqaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
#         likes = data.get('totalShareStatistics', {}).get('likeCount', 0)
#         comments = data.get('totalShareStatistics', {}).get('commentCount', 0)
#         shares = data.get('totalShareStatistics', {}).get('shareCount', 0)
#         return likes, comments, shares
#     else:
#         # Handle errors here
#         print("Error fetching engagement data:", response.text)
#         return None, None, None




# def GenerateAILinkedInPost(request):
#     if request.method == 'GET':
#         access_token = UserAccessToken.objects.filter(user=request.user, types='LinkedIn').first()
#         if access_token:
#             token = access_token.token
#             linkedin_pages = get_linkedin_pages(token)
#             page_engagement_data = []
#             for page in linkedin_pages:
#                 page_id = page['id']
#                 page_name = page['name']
#                 likes, comments, shares = get_page_engagement(token, page_id)
#                 page_engagement_data.append({
#                     'name': page_name,
#                     'id': page_id,
#                     'likes': likes,
#                     'comments': comments,
#                     'shares': shares
#                 })
#             return render(request, 'generatepost.html', {'linkedin_pages': page_engagement_data})
#         else:
#             # Handle case where user has no LinkedIn access token
#             return render(request, 'generatepost.html')



# def GenerateAILinkedInPost(request):

#     if request.method == 'GET':
#         access_token = UserAccessToken.objects.filter(user=request.user, types='LinkedIn').first()
#         if access_token:
#             token = access_token.token
#             # Get LinkedIn pages
#             linkedin_pages = get_linkedin_pages(token)
#             print("ttttttttttttttttttttttttttttt", linkedin_pages) 

#             # Pass the LinkedIn pages data to the template for rendering
#             return render(request, 'generatepost.html', {'linkedin_pages': linkedin_pages})
#         else:
#             # Handle case where user has no LinkedIn access token
#             return render(request, 'generatepost.html')
    
    




# ----------------------------------------------------End_get_linkedin_page---------------------------------------------


#--------------------------------------instagram page/detail get---------------------------------------#

def get_insta_pages(request):
    # access_token = 'EAAZALWvsrG0oBOymaZApvrkZArCcO9M0IoIODXcpCCTMSZBeP2D3YqwU5ZCmZCETirYDhoCxfVTGpZB2AmUOx1LxMKgmqPy31ySSpAgW4liVFZAM1GjvOECNHD8dEspKkcIeQLnAnsvDe36abZCEK6APzt4lZAB1e8EiiSifAXox183H6ORtcCZBonOw0yBGKIH8mcyO44C7WGnJtxxZCjZAUOSmboO4Q4dZCbNFqKPxyWZB5I1oZC99FYmj5IXy0RhqAEJS'
    access_token = UserAccessToken.objects.filter(user=request.user,types='Facebook').first()
    print(access_token,'----------------------access_token')
    data = get_instagram_accounts(access_token)
    print(data.text)










def get_linkedin_data(request,id):
    try:
        user_access_token = UserAccessToken.objects.filter(user__generate_user__id=id, types='LinkedIn').first()
        if user_access_token:
            access_token = user_access_token.token
        else:
            return JsonResponse({"error": "Access token not found."})

        generate_post = GeneratePost.objects.filter(id=id).first()
        if generate_post:
            post_id = generate_post.linkedin_page_video_id or generate_post.linkedin_page_image_id  # Assuming linkedin_page_id is the post ID
        else:
            return JsonResponse({"error": "Post ID not found."})

        # The API endpoint for retrieving post details
        url = f'https://api.linkedin.com/v2/socialActions/{post_id}'

        # The headers including the authorization token
        headers = {
            'Authorization': f'Bearer {access_token}',
            'LinkedIn-Version': '202402'   # LinkedIn API version
        }
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            likes_summary = data.get('likesSummary', {})
            comments_summary = data.get('commentsSummary', {})

            engagement_data = {
                "likes": likes_summary.get('totalLikes', 0),
                "comments": comments_summary.get('totalFirstLevelComments', 0),
                "shares": data.get('distribution', {}).get('shareCount', 0)
            }
            return JsonResponse(engagement_data)
        else:
            return JsonResponse({"error": f"Failed to retrieve data: {response.status_code}, {response.text}"})

    except Exception as e:
        return JsonResponse({"error": f"An error occurred: {str(e)}"})
    



def get_instagram_metrics(request, id):
    try:
        user_access_token = UserAccessToken.objects.filter(user__generate_user__id=id, types='Facebook').first()
        if user_access_token:
            access_token = user_access_token.token
        else:
            return JsonResponse({"error": "Access token not found."})

        generate_post = GeneratePost.objects.filter(id=id).first()
        if generate_post:
            if generate_post.instagram_page_post_id:
                media_id = generate_post.instagram_page_post_id
            elif generate_post.instagram_page_video_id:
                media_id = generate_post.instagram_page_video_id
            else:
                return JsonResponse({"error": "Neither Post ID nor Video ID found."})
        else:
            return JsonResponse({"error": "Post ID not found."})

        api_version = 'v19.0'
        fields = 'comments_count,like_count,insights.metric(engagement,impressions,reach,saved,video_views)'
        # fields = 'comments_count,like_count'

        url = f'https://graph.facebook.com/{api_version}/{media_id}?fields={fields}&access_token={access_token}'

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                likes = data.get('like_count', 0)
                comments = data.get('comments_count', 0)
                shares = 'Not directly available'
                views = data.get('video_views', 0) if 'video_views' in data else 'Not available'
                return JsonResponse({'likes': likes, 'comments': comments, 'shares': shares})
            else:
                error_message = response.text
                return JsonResponse({'error': f'Request failed with status code {response.status_code}: {error_message}'})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    except Exception as e:
        return JsonResponse({'error': str(e)})


