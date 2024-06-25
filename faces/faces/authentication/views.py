from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from authentication.models import CustomUser as User,Category,TeamMember,SocialMediaSection,Appointment,SocialMediaFile,StaticPrompts,Prompt,Payment,Voucher,VoucherUsage,GenerateCategoryPrompt,CaseFilePrompt,GenerateCaseFilePrompt,MediaPrompt
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
from pyfacebook import GraphAPI
import uuid
import os
import requests
from face.settings import BASE_URL
from social_media_post.models import UserAccessToken
from authentication.permissions import admin_only
from .helper import StringEncoder






def index(request):

    first_name = ''
    last_name = ''
    username = ''
    email = ''

    if request.user.is_authenticated:
        user = request.user
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        email = user.email

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username,
        'email': email,
        'partner_id': 'faces',  # You can set this to whatever value you need
    }
    return render(request, 'index.html', context)



# @admin_only
def signup(request):

    lists = CompanyList.objects.all()
  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        # company_list_id = request.POST.get('company_list')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different username."
            return JsonResponse({'success': False, 'message': error_message,  'icon': True}, status=200)
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            error_message = "Email already exists. Please use a different email address."
            return JsonResponse({'success': False, 'message': error_message, 'icon': True}, status=200)
        # Create user
        new_user =User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        # Save the selected company list to the user
        # if company_list_id:
        #     company_list = CompanyList.objects.get(id=company_list_id)
        #     new_user.company = company_list
        #     new_user.save()

        success_message = "Signup successful. You can now login."
        return HttpResponse(success_message)

    return render(request, 'signup.html', {'lists': lists})





def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            success_message = "Login successful"
            return HttpResponse(success_message)

        else:
            error_message = "Invalid username or password. Please try again."
            return JsonResponse({'success': False, 'message': error_message}, status=500)

          

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')




User = get_user_model()

class CustomPasswordResetView(View):
    template_name = 'password_reset.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_message = {"error": "User with this email does not exist."}
            return JsonResponse(error_message, status=400)

        else:
            self.send_reset_email(request, user)
        success_message = "Password reset email has been sent."
        return HttpResponse(success_message)

       

    def send_reset_email(self, request, user):
        user_id_bytes = str(user.id).encode('utf-8')

        encoded_user_id = base64.b64encode(user_id_bytes).decode('utf-8')
        print(encoded_user_id,'encoded_user_idencoded_user_id')
        reset_url = reverse('password_reset_confirm', kwargs={'user_id': encoded_user_id})

        subject = 'Password Reset'
        message = render_to_string('authentication/templates/password_reset_email.txt', {
            'user': user,
            'reset_url': request.build_absolute_uri(reset_url),
        })

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])





class CustomPasswordResetConfirmView(View):
    def get(self, request, user_id, *args, **kwargs):
        user_id_bytes = base64.b64decode(user_id.encode('utf-8'))
        user_id = int(user_id_bytes.decode('utf-8'))
        return render(request,"password_reset_confirm.html",{'user_id':user_id})
        
      

    def post(self, request, user_id, *args, **kwargs):
        user = User.objects.get(id=user_id)
        new_password = request.POST.get('password')
        user.set_password(new_password)
        user.save()

        return JsonResponse({'message': 'Password reset successful. You can now log in with your new password.'})
    

def privacypolicy(request):
    return render(request, 'privacy.html')




# ---- linkdin function for login(orignal)---#

from django.core.cache import cache

def LinkeInAuthentication(request):
    url = f"{settings.LINKEDIN_BASE_URL}?response_type=code&client_id={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY}&state=random&redirect_uri={settings.LINKEDIN_REDIRECT_URL}&scope={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE}"
    return redirect(url)

# def LinkeInAuthentication(request, force_reauth=True):    
#     if not  force_reauth:
#         return render(request, 'Re-authenticate.html')
#     auth_url = f"{settings.LINKEDIN_BASE_URL}?response_type=code&client_id={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY}&state=random&redirect_uri={settings.LINKEDIN_REDIRECT_URL}&scope={settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE}"
#     return redirect(auth_url)




def LinkedInAcessToken(request):
    auth_code = request.GET.get("code",None)
    if auth_code:
        payload = {
            'grant_type' : 'authorization_code',
            'code' : auth_code,
            'redirect_uri' : settings.LINKEDIN_REDIRECT_URL,
            'client_id' : settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY,
            'client_secret' : settings.SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET
        }
        response = requests.post(url=settings.LINKEDIN_ACCESS_URL, params=payload)
        response_json = response.json()
        user_token = UserAccessToken.objects.filter(user=request.user,types='LinkedIn')
        if user_token:
            new_user_token = user_token.first()
            new_user_token.token =  response_json['access_token']
            new_user_token.save()

                        
        else:
            user_token = UserAccessToken.objects.create(user=request.user,types='LinkedIn',token=response_json['access_token'])
            user_token.save()
        access_token = response_json['access_token']
        return redirect('/')
    return HttpResponse("something went wrong")












#-------------------------------Start instagram python code--------------------------



def authenticate_with_instagram(request):

    client_id = '1771703993310026'  # Your Meta app ID
    redirect_uri = 'https://ddivesocial.com/facebook-auth-callback/'
    scope = 'instagram_basic,instagram_content_publish,instagram_manage_comments,instagram_manage_insights,pages_show_list,pages_read_engagement'
    # Constructing the URL
    url = f"https://www.facebook.com/dialog/oauth?client_id={client_id}&display=page&extras=%7B%22setup%22%3A%7B%22channel%22%3A%22IG_API_ONBOARDING%22%7D%7D&redirect_uri={redirect_uri}&response_type=token&scope={scope}"
    # Redirecting user to Instagram business login
    return redirect(url)


    

#-------------------------------End instagram python code--------------------------



#-----------------------------facebook python code -----------#



from django.shortcuts import redirect, render
from django.conf import settings
import requests
from urllib.parse import urlparse, parse_qs

app_id = '1771703993310026'
app_secret = 'ea6e4300df0e6087d9d6df63ac12bd84'
redirect_uri = 'https://ddivesocial.com/facebook-auth-callback/'


def authenticate_with_facebook(request):
    auth_url = f'https://www.facebook.com/v12.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope=business_management,email,public_profile'
    return redirect(auth_url)

def facebookInAcessToken(request):
    auth_code = request.GET.get("code", None)

    if auth_code:
        token_url = f'https://graph.facebook.com/v12.0/oauth/access_token?client_id={app_id}&redirect_uri={redirect_uri}&client_secret={app_secret}&code={auth_code}'
        response = requests.get(token_url)
        data = response.json()

        if 'access_token' in data:
            access_token = data['access_token']

            user_info_url = f'https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={access_token}'
            user_info_response = requests.get(user_info_url)
            user_info = user_info_response.json()

            # Filter instead of get to avoid MultipleObjectsReturned error
            user_tokens = UserAccessToken.objects.filter(user=request.user, types='Facebook')

            if user_tokens.exists():
                user_token = user_tokens.first()
            else:
                # If no token exists, create a new one
                user_token = UserAccessToken.objects.create(user=request.user, types='Facebook')

            user_token.token = access_token
            user_token.save()

            return redirect('/')
        else:
            return redirect('/')  
    else:
        return redirect('/')
        # return HttpResponse("Something went wrong")  







# def authenticate_with_facebook(request):
#     # if request.method == 'GET':
#         auth_url = f'https://www.facebook.com/v12.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope=business_management,email,public_profile'
#         return redirect(auth_url)



# def facebookInAcessToken(request):
#     auth_code = request.GET.get("code", None)

#     token_url = f'https://graph.facebook.com/v12.0/oauth/access_token?client_id={app_id}&redirect_uri={redirect_uri}&client_secret={app_secret}&code={auth_code}'
#     response = requests.get(token_url)
#     data = response.json()
#     access_token = data['access_token']

#     user_info_url = f'https://graph.facebook.com/v12.0/me?fields=id,name,email&access_token={access_token}'
#     user_info_response = requests.get(user_info_url)
#     user_info = user_info_response.json()

#     if auth_code:
#         user_token = UserAccessToken.objects.filter(user=request.user, types='Facebook')
#         if user_token:
#             new_user_token = user_token.first()
#             new_user_token.token = access_token
#             new_user_token.save()

#         else:
#             user_token = UserAccessToken.objects.create(user=request.user, types='Facebook',
#                                                         token=access_token)
#             user_token.save()
#         access_token = access_token
#         return redirect('/')
#     return HttpResponse("something went wrong")











# def CreatePost(request):
#     if request.method == 'POST':
#         titl1e = request.POST.get('title')
#         print("herer is ",titl1e)
#         post_date = request.POST.get('post_date')
#         image = request.FILES.get('image')
#         option = request.POST.get('option')
#         description = request.POST.get('description')

#         item = PostList.objects.create(title=titl1e, post_date=post_date, image=image, option=option, description=description)
#         item.save()
#         try:
#             post_on_facebook(titl1e, description)  # Assuming image.url is the URL of the image
#         except Exception as e:
#             # Handle exceptions here
#             print("Failed to post on Facebook:", e)
#         return redirect('list')
#     return render(request, 'createpost.html')

# def post_on_facebook(titl1e, description):
#     # Initialize the GraphAPI with your access token
#     graph = GraphAPI(access_token=settings.FACEBOOK_ACCESS_TOKEN)
    
#     # Define the parameters of the post
#     params = {
#         'message': titl1e + "\n\n" + description
#     }
    
#     # If there's an image, add it to the parameters
    
#     # Post to Facebook
#     graph.put_object(parent_object='me', connection_name='feed', **params)
# # post_on_facebook("Title", "Description", "https://example.com/image.jpg")





# def ItemList(request):
#     item = PostList.objects.all()
#     return render(request,'list.html',{'item':item})

# def update_item(request, pk):
#     item = get_object_or_404(PostList, pk=pk)
#     if request.method == 'POST':
#         item.title = request.POST['title']
#         item.post_date = request.POST['post_date']
#         if 'image' in request.FILES:
#             item.image = request.FILES['image']
#         item.option = request.POST['option']
#         item.description = request.POST['description']
#         item.save()
#         return redirect('list')
#     return render(request, 'update.html', {'item': item})


# def delete_item(request, pk):
#     item = get_object_or_404(PostList, pk=pk)
#     item.delete()
#     return redirect('list')
   


from .models import CompanyList

def CompanyLists(request):
    lists = CompanyList.objects.all()
    return render(request, 'signup.html', {'lists': lists})


#calender
def calenderview(request):
    return render(request,'Calendar.html')




##########----------------SHIVAM--------------############
from social_media_post.models import GeneratePost

# def PostView(request, pk):
#     item = get_object_or_404(GeneratePost, pk=pk)
#     return render(request, 'generatepostview.html', {'item': item})



def PostView(request, pk):
    item = get_object_or_404(GeneratePost, pk=pk)
    if request.method == 'POST':
        # Handle form submission
        item.name = request.POST.get('name')
        item.post_date = request.POST.get('post_date')
        item.description = request.POST.get('description')
        # Handle other fields similarly

        item.save()
        return redirect('post_detail', pk=pk)  # Redirect to the detail view after editing

    return render(request, 'generatepostview.html', {'item': item})








def LogoutLinkedinUser(request):
    # Call LinkedIn logout API
    linkedin_logout_url = "https://www.linkedin.com/m/logout/"
    response = requests.get(linkedin_logout_url)

    # Check if the logout request was successful (you may need to adjust this based on the response status or content)
    print("11111111111111111111111111",response.status_code)
    if response.status_code == 200:
        
        print("Successfully logged out from LinkedIn")
        # Redirect the user regardless of the result of the API call
        return redirect('/')










#----------------------company creation code-------------------------------------#

from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, CompanyList, TeamMember
from django.http import HttpResponseBadRequest
from django.utils.text import slugify
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from authentication.permissions import has_paid_shares
from django.contrib.auth.decorators import user_passes_test

# View for creating a company
@user_passes_test(has_paid_shares)


def company_create(request):
    Backend_url= BASE_URL
    categories = Category.objects.all()
    team_members = TeamMember.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        title = title.lower()
        print(title,'uuuuuuuuuuuus')
        description = request.POST.get('description')
        # category_id = request.POST.get('category_id')
        media = request.FILES.get('media')

        if title and description :
            if title and description:
                # category = get_object_or_404(Category, pk=category_id)
                try:
                    company_instance = CompanyList.objects.create(title=title, description=description, media=media)
                    if company_instance:
                        user = User.objects.get(id=request.user.id)
                        user.company = company_instance
                        user.save()
                        
                except IntegrityError:
                    # Handle the case where the title is not unique
                    error_message = "A company with the same title already exists. Please choose a different title."
                    return JsonResponse({'success': False, 'error_message': error_message},status=400)
                else:
                    company_title = company_instance.title
                    company_title = slugify(company_title)
                    return JsonResponse({'success': True, 'company_name': company_title,'id':company_instance.id},status=200)

    return render(request, 'company.html',{'categories': categories,'team_members': team_members,'Backend_url':Backend_url})
    # return JsonResponse({'success': True, 'message': 'Company created Successfully.'},status=201)


def company_edit(request, company_id):
    company_instance = get_object_or_404(CompanyList, id=company_id)
    team_member = request.user.company.member_company.first()
    Backend_url= BASE_URL

    if request.method == 'POST':
        print(request.POST,'popopopjjjjj')
        # title = request.POST.get('title')
        # title = title.lower()
        description = request.POST.get('description')
        media = request.FILES.get('media')
        print(request.FILES,'----------------------media')

        if description:
            try:
                # company_instance.title = title
                company_instance.description = description

                if media:
                    print('Media is present, attempting to save...')
                    company_instance.media = media
                    company_instance.save()
                    print('Media saved successfully.')
                else:
                    company_instance.save()
            except IntegrityError:
                error_message = "A company with the same title already exists. Please choose a different title."
                return JsonResponse({'success': False, 'error_message': error_message}, status=400)
            else:
                company_title = company_instance.title
                company_title = slugify(company_title)
                return JsonResponse({'success': True, 'company_name': company_title, 'id': company_instance.id}, status=200)

    return render(request, 'company_edit.html', {'company': company_instance,'team_member':team_member,'Backend_url':Backend_url})


def Companyalldetails(request):
    user=request.user
    user_company  = user.company
    print(user_company,'user_companyuser_company------------')

     # Check if user_company and associated team member exist
    if user_company:
        team_member = user_company.member_company.first()  # Assuming there's only one team member per company
        if team_member:
            team_member_id = team_member.id
            team_member_capacity = team_member.capacity
            team_member_availability_start = team_member.availability_start
            team_member_availability_end = team_member.availability_end
        else:
            team_member_id=None
            team_member_capacity=None
            team_member_availability_start=None
            team_member_availability_end=None

        # Initialize social_media_id
        social_media_id = None
        social_category=''
        social_prompts=''
        case_files=''
        

        # Retrieve the SocialMediaSection associated with the company
        if hasattr(user_company, 'user_company_social'):
            social_media_section = user_company.user_company_social.first()
            if social_media_section:
                social_media_id = social_media_section.id
                # Get selected social categories and prompts
                social_category = list(social_media_section.category.all().values('name'))
                social_prompts = list(social_media_section.prompts.all().values('text','id'))
                case_files =[{"id":file.id,"file_name": file.case_file.file.name} for file in social_media_section.files.all()]
                case_prompts =[{"id":file.id,"file_name": file.text} for file in social_media_section.case_file_prompts.all()]


        data = {
            'title':user_company.title,
            'id':user_company.id,
            'description':user_company.description,
            'media': user_company.media.file.name if user_company.media else None,
            'team_member_id':team_member_id,
            'team_member_capacity':team_member_capacity,
            'team_member_availability_start':team_member_availability_start,
            'team_member_availability_end':team_member_availability_end,
            'social_media_id':social_media_id,
            'social_description':social_media_section.description if social_media_section else None,
            'social_category':social_category,
            'social_prompts':social_prompts,
            'case_files':case_files,
            'case_prompts':case_prompts
        }
        return JsonResponse({'data':data},status=200)




def company_detail(request, company_name):
    # print(company_name)
    Backend_url= BASE_URL
   
    # company = get_object_or_404(CompanyList, title=company_name.replace('-', ' '))
    # team_member = TeamMember.objects.get(company__title=company)
    # company.url = f'http://127.0.0.1:8000/{company_name}'
    # company.save()
    return render(request, 'company_detail.html',{'Backend_url':Backend_url})
    

def company_all_details(request,company_name):

    company_name =  company_name
    # print(company_name,'iiiiiiiiiiiiiiii')
    try:
       
        company = get_object_or_404(CompanyList, title=company_name.replace('-', ' '))
        team_member = TeamMember.objects.get(company__title=company)
        company.url = f'{BASE_URL}/{company_name}'
        company.save()

         # Convert datetime objects to strings with date and time separately
        availability_start_date = team_member.availability_start.strftime('%Y-%m-%d')
        availability_start_time = team_member.availability_start.strftime('%H:%M:%S')
        availability_end_date = team_member.availability_end.strftime('%Y-%m-%d')
        availability_end_time = team_member.availability_end.strftime('%H:%M:%S')
        
        data = {
            'company': {
                'name': company.title,
                'description': company.description,
                'media': company.media.url if company.media else ''
                # Add other fields you want to include
            },
            'team_member': {
                'name': team_member.capacity,
                'availability_start_date': availability_start_date,
                'availability_start_time': availability_start_time,
                'availability_end_date': availability_end_date,
                'availability_end_time': availability_end_time
                # Add other fields you want to include
            }
        }
        
        return JsonResponse(data)
    except Exception as e:
        # Handle exceptions, return appropriate error response
        return JsonResponse({'error': str(e)}, status=500)

# View for rendering the company creation page
# def categories(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         print('=================categories')
#         return render(request, 'company.html', {'categories': categories})

# View for rendering the team member list page
# def team_member_list(request):
#     team_members = TeamMember.objects.all()
#     return render(request, 'team_member_list.html', {'team_members': team_members})

def team_member_add(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        # print(request.POST,'popopopopop')
        availability_start = request.POST.get('availability_start')
        availability_end = request.POST.get('availability_end')
        company_id = request.POST.get('company_id')
        if name:
            new_member = TeamMember.objects.create(capacity=name, availability_start=availability_start,availability_end=availability_end,company_id=company_id)
            return JsonResponse(
                {'success': True, 'message': 'Team member added successfully', 'member_id': new_member.id})
        else:
            return JsonResponse({'success': False, 'message': 'Name field is required'})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'})

def team_member_list(request):
    team_members = TeamMember.objects.filter(company=request.user.company)
    # print(request.user.company,'popopopopop')

    team_members_data = []

    for member in team_members:
        # Create a dictionary for each team member
        member_data = {
            "id":member.id,
            "name": member.capacity,
            "availability_start": member.availability_start,
            "availability_end": member.availability_end
        }
        # Append the member data to the list
        team_members_data.append(member_data)
    # Return JSON response
    return JsonResponse({'team_members': team_members_data})

# View for editing a team member
def team_member_edit(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        availability_start = request.POST.get('availability_start')
        availability_end = request.POST.get('availability_end')
        if name:
            member.capacity = name
            member.availability_start = availability_start
            member.availability_end = availability_end
            member.save()
            return JsonResponse({'success': True, 'message': 'Team member updated successfully'})
        else:
            return JsonResponse({'success': False, 'message': 'Name field is required'})
    else:
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed'})


# View for deleting a team member
def team_member_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'DELETE':
        member.delete()
        return JsonResponse({'success': True, 'message': 'Team member deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
    

def get_particular_member(request,pk):
    member = get_object_or_404(TeamMember, pk=pk)
    data={
        "id":member.id,
        "name":member.name,
        "availability": member.availability,
    }
    return JsonResponse({'team_members': data})



def social_media_post(request):
    if request.method == 'POST':
        print(request.POST,'===========================mediaaa')
        media_prompt_ids = request.POST.getlist('uploadedcase')
        company = request.POST.get('businessfacts')
        prompt_ids = request.POST.getlist('propertystrategies')
        # keywords = request.POST.get('Keywords')
        category_ids = request.POST.getlist('category')
        company_id = request.POST.get('company_id')
        files = request.FILES.getlist('Brochuremedia')  # Access multiple uploaded files
        # print(files,'ppppp')

        # Create the SocialMediaSection instance
        social_media_section = SocialMediaSection.objects.create(
            description=company,
            # keywords=keywords,
            user=request.user,
            company_id=company_id
        )

        #media_prompts
        media_prompts = CaseFilePrompt.objects.filter(id__in=media_prompt_ids)
        social_media_section.case_file_prompts.add(*media_prompts)

        # Associate prompts with the created SocialMediaSection
        prompts = Prompt.objects.filter(id__in=prompt_ids)
        social_media_section.prompts.add(*prompts)

        # Associate categories with the created SocialMediaSection
        categories = Category.objects.filter(id__in=category_ids)
        social_media_section.category.add(*categories)

        #associate categories with the created company
        company_category = CompanyList.objects.get(id=company_id)
        # print(company_category)
        categories = Category.objects.filter(id__in=category_ids)
        company_category.category.add(*categories)

        # Save the uploaded files
        for file in files:
            SocialMediaFile.objects.create(
                social_media_section=social_media_section,
                case_file=file
            )

        return JsonResponse({'success': True}, status=200)
        

def edit_social_media_post(request):
    Backend_url= BASE_URL

    return render(request,'company_edit.html',{'Backend_url':Backend_url})


def edit_social_media_post(request, post_id):
    Backend_url = BASE_URL
    if request.method == 'POST':
        print(request.POST,'p-p-p-p-')
        case_file_ids = request.POST.getlist('uploadedcaseCasePrompt')
        company = request.POST.get('businessfacts')
        prompt_ids = request.POST.getlist('propertystrategies')
        category_ids = request.POST.getlist('category')
        company_id = request.POST.get('company_id')
        files = request.FILES.getlist('Brochuremedia')  # Access multiple uploaded files

        if post_id:
            # Fetch the existing SocialMediaSection instance for editing
            social_media_section = get_object_or_404(SocialMediaSection, id=post_id)
        else:
            # Create a new SocialMediaSection instance
            social_media_section = SocialMediaSection(
                description=company,
                company_id=company_id,
                user=request.user
            )
            social_media_section.save()

        social_media_section.description = company
        social_media_section.company_id = company_id
        social_media_section.user = request.user
        social_media_section.save()

        # Clear existing relationships and add new ones
        social_media_section.prompts.clear()
        prompts = Prompt.objects.filter(id__in=prompt_ids)
        social_media_section.prompts.add(*prompts)

        social_media_section.case_file_prompts.clear()
        prompts = CaseFilePrompt.objects.filter(id__in=case_file_ids)
        print(prompts,'gggggggggggggggggggggggggggggcasefilessssssss')
        social_media_section.case_file_prompts.add(*prompts)

        social_media_section.category.clear()
        categories = Category.objects.filter(id__in=category_ids)
        social_media_section.category.add(*categories)

        # Associate categories with the company
        company_category = get_object_or_404(CompanyList, id=company_id)
        company_category.category.clear()
        categories = Category.objects.filter(id__in=category_ids)
        company_category.category.add(*categories)

        # Save the uploaded files
        # If editing, clear old files before adding new ones
        # SocialMediaFile.objects.filter(social_media_section=social_media_section).delete()

        for file in files:
            SocialMediaFile.objects.create(
                social_media_section=social_media_section,
                case_file=file
            )

        return JsonResponse({'success': True}, status=200)
    else:
        return render(request, 'company_edit.html', {'Backend_url': Backend_url})
    # if request.method == 'POST':
    #     company = request.POST.get('businessfacts')
    #     prompt_ids = request.POST.getlist('propertystrategies')
    #     category_ids = request.POST.getlist('category')
    #     company_id = request.POST.get('company_id')
    #     files = request.FILES.getlist('Brochuremedia')  # Access multiple uploaded files

    #     # Fetch the existing SocialMediaSection instance for editing
    #     social_media_section = get_object_or_404(SocialMediaSection, id=post_id)
    #     social_media_section.description = company
    #     social_media_section.company_id = company_id
    #     social_media_section.user = request.user
    #     social_media_section.save()

    #     # Clear existing relationships and add new ones
    #     social_media_section.prompts.clear()
    #     prompts = Prompt.objects.filter(id__in=prompt_ids)
    #     social_media_section.prompts.add(*prompts)

    #     social_media_section.category.clear()
    #     categories = Category.objects.filter(id__in=category_ids)
    #     social_media_section.category.add(*categories)

    #     # Associate categories with the company
    #     company_category = get_object_or_404(CompanyList, id=company_id)
    #     company_category.category.clear()
    #     categories = Category.objects.filter(id__in=category_ids)
    #     company_category.category.add(*categories)

    #     # Save the uploaded files
    #     # If editing, clear old files before adding new ones
    #     SocialMediaFile.objects.filter(social_media_section=social_media_section).delete()
        
    #     for file in files:
    #         SocialMediaFile.objects.create(
    #             social_media_section=social_media_section,
    #             case_file=file
    #         )

    #     return JsonResponse({'success': True}, status=200)
    # else:
    #     return render(request, 'company_edit.html', {'Backend_url': Backend_url})



import requests
import os
from openai import OpenAI
import json

# OPEN_API_KEY = os.getenv('OPEN_API_KEY')
# client = OpenAI(api_key=OPEN_API_KEY)






def generate_category_prompt(text):

    prompt_data = GenerateCategoryPrompt.objects.first()
   
    # print(type(prompt_data.prompt),'][][][]')

    if prompt_data and hasattr(prompt_data, 'prompt'):
        # Use str.format to dynamically insert the text
        prompts = prompt_data.prompt.format(text=text)

        # print(prompts,'[[[[[[prompts]]]]]]')

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompts,
        max_tokens=800
    )
    prompt_list = response.choices[0].text.strip()
    return prompt_list


def generate_prompt(request):
    data=json.loads(request.body)
    category_ids=data['category_ids']
    print(category_ids,'category_idscategory_idscategory_ids')
    # category = Category.objects.get(id=pk)
    category_text = []
    serialized_prompts = []
    case_files = []
    files = SocialMediaFile.objects.filter(social_media_section__user=request.user)
    for i in files:
        file_name = os.path.basename(i.case_file.name)
        data = {
            'files':file_name
        }
        case_files.append(data)

    for i in category_ids:
        category_data = Category.objects.get(id=i)
        text = {
            'text':category_data.text,
            'category_name':category_data.name,
            'category_id':category_data.id
        }
        category_text.append(text)
    print(category_text,'textttttttt')


    combined_text=[]
    if category_text:
        for i in category_text:
            category_id = i['category_id']
            combined_texts = " and combine ".join([i['text'] for i in category_text])
            if combined_texts not in combined_text:
                combined_text.append(combined_texts)

            # print(combined_text,'=======combined_textcombined_text')

            # print(1+'1')
            # text = i['text']
           
        prompts = generate_category_prompt(combined_text)
        # print(prompts,'generaeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')

        # prompts = generate_category_prompt(category_name)
        if prompts:
            prompt_list = prompts.split('\n')
            # print(prompt_list,'prompt_listprompt_list')
            # print(prompt_list,'prompt_listprompt_list')
            # Create a list of dictionaries containing index and prompt
            indexed_prompts=[]
            for prompt in prompt_list:
                # data = prompt.strip()
                # indexed_prompts.append(data)
                indexed_prompts.append(Prompt(category_id=category_id, text=prompt.strip()))

            # Bulk create the prompts
            created_prompts = Prompt.objects.bulk_create(indexed_prompts)

            # Serialize the necessary data
            # serialized_prompts = [{'category': prompt.category.name, 'text': prompt.text,'id':prompt.id} for prompt in indexed_prompts]
            # Serialize the created prompts and add them to the list
            serialized_prompts.extend([{'category': prompt.category.name, 'text': prompt.text, 'id': prompt.id} for prompt in created_prompts])


        # return JsonResponse({'prompts': serialized_prompts})
        return JsonResponse({'prompts': serialized_prompts,'case_files':case_files})


            # return JsonResponse(indexed_prompts,safe=False)
            # return JsonResponse({'prompt':prompts})
    else:
        return JsonResponse({'message':'Please select category.'})

from django.core import serializers

def StaticPromptdata(request):
    datas = StaticPrompts.objects.all()
    dataa = []
    for i in datas:
        dataa.append((i.personal_development))
        dataa.append((i.meeting_attended))
        # data = {
        #     'personal_development':i.personal_development,
        #     'meeting_attended':i.meeting_attended
        # }
        # dataa.append(data)
    return JsonResponse({'data': dataa})

def get_unique_prompts(request):
    user_company = request.user.company
    print(user_company,'---------user_company')

    # Retrieve all category IDs associated with the user's company
    company_categories = user_company.category.values_list('id', flat=True)
    print(company_categories,'company_categories')
    static_prompts = list(StaticPrompts.objects.all().values())  # Convert StaticPrompts queryset to a list of dictionaries
    comp_categories=[]
    all_case_files = []  # List to store all case files of the user
    # static_prompts=[]
    for i in company_categories:
        comp_categories.append(i)

    # sections = SocialMediaSection.objects.filter(company=user_company, prompts__category__in=comp_categories).distinct()
    sections = SocialMediaSection.objects.filter(company=user_company, user=request.user).distinct()

    printed_prompts = set()
    printed_categories = set()
    printed_casefiles = set()
    unique_prompts = []
    unique_categories = []
    unique_casefileprompt = []

    for section in sections:
        prompts = section.prompts.all()
        print(prompts,'-------prompts')
        categories = section.category.all()
        files = section.files.all()  # Retrieve all case files associated with the section
        case_prompts = section.case_file_prompts.all()


        for case in case_prompts:
            if case.text not in printed_casefiles:
                unique_casefileprompt.append({"text": case.text,"prompt_id":case.id})
                printed_casefiles.add(case.text)
        
        for prompt in prompts:
            print(prompt,'-0-0-0-0-0-')
            if prompt.text not in printed_prompts:
                unique_prompts.append({"text": prompt.text,"prompt_id":prompt.id})
                printed_prompts.add(prompt.text)

        for category in categories:
            if category.id not in printed_categories:
                unique_categories.append({"id": category.id, "name": category.name,"keywords":category.keywords})
                printed_categories.add(category.id)

        for file in files:
            file_name = os.path.basename(file.case_file.name)
            all_case_files.append({"file_name": file_name,'id':file.id})
            
        # for i in static_prompt:
        #     static_prompts.append(i)

    response_data = {
        "prompts": unique_prompts,
        "categories": unique_categories,
        "case_files": all_case_files,
        "static_prompts":static_prompts,
        "case_file_prompts":unique_casefileprompt
    }

    return JsonResponse(response_data, safe=False)
    # user_category_id = request.user.company.category.id
    # print(user_category_id,'user_category_id')
    # sections = SocialMediaSection.objects.filter(company=user_company, prompts__category=user_category_id).distinct()
    # printed_prompts = set()  # Set to keep track of printed prompts
    # printed_categories = set()  # Set to keep track of printed categories
    # unique_prompts = []  # List to store unique prompts
    # unique_categories = [] 
    # for section in sections:
    #     prompts = section.prompts.all()
    #     categories = section.category.all()
    
    #     for prompt in prompts:
    #         if prompt.text not in printed_prompts:  # Check if the prompt has not been printed yet
    #             unique_prompts.append({"text": prompt.text})
    #             printed_prompts.add(prompt.text)

    #     for category in categories:
    #         if category.id not in printed_categories:  # Check if the category has not been printed yet
    #             unique_categories.append({"id": category.id, "name": category.name})
    #             printed_categories.add(category.id)

    # response_data = {
    # "prompts": unique_prompts,
    # "categories": unique_categories
    # }

    # # Serialize the data to JSON
    # response_json = json.dumps(response_data)


    # # Return JSON response
    # return JsonResponse(response_json, safe=False)

from datetime import datetime
def book_slot(request):
    # name = request.POST.get('slotname')
    # email = request.POST.get('slotemail')
    # mobile = request.POST.get('slotmobile')
    # start_time = request.POST.get('start_time')
    # print(start_time)
    # end_time = request.POST.get('end_time')
    # print(end_time)
    # availability_start = request.POST.get('availability_start_date')
    # print(availability_start +' '+ start_time )
    # availability_start = availability_start +' '+ start_time 
    # availability_end = request.POST.get('availability_end_date')
    # print(availability_end)
    # availability_end = availability_end +' '+ end_time 
    # capacity = request.POST.get('capacity')
    # print(capacity,'popopop')

    # # Check if the slot is already fully booked within the specified time frame
    # if Appointment.objects.filter(availability_start__lte=availability_start, availability_end__gte=availability_end).count() >= capacity:
    #     return JsonResponse({'success': False, 'message': 'Slot fully booked'})
    # else:
    #     # Check if the requested time frame is already fully booked
    #     if Appointment.objects.filter(availability_start=availability_start, availability_end=availability_end).count() >= capacity:
    #         return JsonResponse({'success': False, 'message': 'Slot fully booked at this time'})
    #     else:
    #         # If the slot is available, create a new booking
    #         try:
    #             user = request.user
    #             booking = Appointment.objects.create(name=name,email=email,mobile=mobile,availability_start=availability_start, availability_end=availability_end)
    #             return JsonResponse({'success': True, 'message': 'Slot booked successfully'})
    #         except Exception as e:
    #             return JsonResponse({'success': False, 'message': str(e)})
            
    name = request.POST.get('slotname')
    email = request.POST.get('slotemail')
    mobile = request.POST.get('slotmobile')
    start_time_str = request.POST.get('start_time')  # Assuming the format is "HH:MM am/pm"
    start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
    print(start_time)
    
    # end_time_str = request.POST.get('end_time')  # Assuming the format is "HH:MM am/pm"
    # end_time = datetime.strptime(end_time_str, '%I:%M %p').time()
    # print(end_time)
    
    availability_start_date = request.POST.get('availability_start_date')
    availability_start = datetime.strptime(availability_start_date, '%Y-%m-%d').date()
    print(availability_start)
    availability_start = datetime.combine(availability_start, start_time)
    
    # availability_end_date = request.POST.get('availability_end_date')
    # availability_end = datetime.strptime(availability_end_date, '%Y-%m-%d').date()
    # print(availability_end)
    # availability_end = datetime.combine(availability_end, end_time)
    
    capacity = request.POST.get('capacity')
    print(capacity)

    # # Check if the slot is already fully booked within the specified time frame
    # if Appointment.objects.filter(availability_start__lte=availability_start, availability_end__gte=availability_end).count() >= int(capacity):
    #     return JsonResponse({'success': False, 'message': 'Slot fully booked'},status=400)
    # else:
    #     # Check if the requested time frame is already fully booked
    #     if Appointment.objects.filter(availability_start=availability_start, availability_end=availability_end).count() >= int(capacity):
    #         return JsonResponse({'success': False, 'message': 'Slot fully booked at this time'})
    #     else:
            # If the slot is available, create a new booking
    try:
        user = request.user
        booking = Appointment.objects.create(name=name,email=email,mobile=mobile,availability_start=availability_start)
        return JsonResponse({'success': True, 'message': 'Slot booked successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})



#get_category_list

def category_list(request):
    category = Category.objects.values('name', 'id')
    
    seen_names = set()
    categories = []
    
    for i in category:
        if i['name'] not in seen_names:
            seen_names.add(i['name'])
            data = {'name': i['name'], 'id': i['id']}
            categories.append(data)
    
    return JsonResponse({'success': True, 'data': categories})



#----------------------------------------stripe payment-------------------------------------#
STRIPE_PUBLISHABLE_KEY = 'pk_test_51PBIQJ0213GG69z5UUnDpCAWivxURJZ3NhKLikdrIyqkPLcn4IUZjtlmJwfJ9qspaQV3gBWpqsKvlPvdrEibsjmU00KUSV0YNB'
STRIPE_SECRET_KEY = 'sk_test_51PBIQJ0213GG69z5IF6BEESZCzorUs12neFW4suGUm41HbmmqP7OtODU85PBtL5SzVIi33S3f5ZorWZRCadsu1oe00IDoiGGh7'

# PAYMENT_SUCCESS_URL = 'http://127.0.0.1:8000/success'
# PAYMENT_CANCEL_URL = 'http://127.0.0.1:8000/cancel/'
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View

stripe.api_key = STRIPE_SECRET_KEY


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def get(self, request, *args, **kwargs):
        # price = Price.objects.get(id=self.kwargs["pk"])

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(100) * 100,
                        "product_data": {
                            "name": 'Create Company',
                            "description": 'Company Creations Charge',
                            "images": [
                                # f"{settings.BACKEND_DOMAIN}/{price.product.thumbnail}"
                            ],
                        },
                    },
                    "quantity": '1',
                }
            ],
            metadata={'id': request.user.id},
            mode="payment",
            success_url=f"{settings.BASE_URL}/success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{settings.BASE_URL}/cancel/",
        )
        print(checkout_session,'ppppooolllll')
        return redirect(checkout_session.url)


from django.views.generic import TemplateView
from django.views.generic.base import TemplateView


class SuccessView(TemplateView):
    template_name = "success.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session_id = self.request.GET.get('session_id')
        print(session_id,'--------session_id')

        if session_id:
            try:
                # Retrieve the session from Stripe
                session = stripe.checkout.Session.retrieve(session_id)
                print(session['payment_status'],'-------sessionsession')
                if session['payment_status']:
                    Payment.objects.create(user=self.request.user,is_paid=True)
                context['session'] = session
            except stripe.error.StripeError as e:
                # Handle error appropriately
                context['error'] = str(e)

        return context


class CancelView(TemplateView):
    template_name = "cancel.html"



#----voucher check code--------#

def check_voucher_code(request):

    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        try:
            voucher = Voucher.objects.get(code=code,is_active=True)
        except Voucher.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid voucher code.'}, status=400)

        if not voucher.is_active:
            return JsonResponse({'success': False, 'message': 'Voucher code is not active.'}, status=400)

        if VoucherUsage.objects.filter(voucher_code=voucher, user=request.user, is_used=True).exists():
            return JsonResponse({'success': False, 'message': 'Voucher code already used.'}, status=400)

        # Create a VoucherUsage entry for this user and mark it as used
        VoucherUsage.objects.create(voucher_code=voucher, is_used=True, user=request.user)

        return JsonResponse({'success': True, 'message': 'Voucher code is valid.'}, status=200)


def voucher_page(request):
    return render(request, 'check_voucher.html')



from PyPDF2 import PdfReader
from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
# from langchain.llms import OpenAI
from langchain_community.llms import OpenAI
from openai import OpenAI

from langchain.llms import OpenAI
from langchain_openai import ChatOpenAI

# OPEN_API_KEY = os.getenv('OPEN_API_KEY')
# client = OpenAI(api_key=OPEN_API_KEY)


def get_pdf_text(document_path, start_page=1, final_page=999):
        reader = PdfReader(document_path)
        number_of_pages = len(reader.pages)
        page=''
        for page_num in range(start_page - 1, min(number_of_pages, final_page)):
            page += reader.pages[page_num].extract_text()
    
        return page


def summarize_data(data):
    apikey =OPEN_API_KEY  #new api key adn
    model = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-1106",openai_api_key=apikey)
    print(model,'-p-p-p-p-p-p')
    summary_chain = load_summarize_chain(llm=model, chain_type='map_reduce')
    summarize_document_chain = AnalyzeDocumentChain(combine_docs_chain=summary_chain)
    print('output(AnalyzeDocumentChain):', summarize_document_chain.run(data))
    summary_data = summarize_document_chain.run(data)

    return summary_data


from openai import OpenAI
# OPEN_API_KEY = os.getenv('OPEN_API_KEY')
# # client = OpenAI()
# client = OpenAI(api_key=OPEN_API_KEY)
OPEN_API_KEY = ''
client = ''

def generate_category_prompt(text):

    # prompt_data = GenerateCaseFilePrompt.objects.first()
   
    # # # print(type(prompt_data.prompt),'][][][]')

    # if prompt_data and hasattr(prompt_data, 'prompt'):
    # #     # Use str.format to dynamically insert the text
    #     prompts = prompt_data.prompt.format(text=text)
    prompts=f"Generate 10 prompts of 2 lines according to the {text} from a case file studies."

        # print(prompts,'[[[[[[prompts]]]]]]')

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompts,
        max_tokens=800
    )
    prompt_list = response.choices[0].text.strip()
    return prompt_list

                


#to get case files
def generatedfilesdata(request):

    if request.method == 'POST':
        try:
            case_id = json.loads(request.body)
            serialized_prompts = []

            for case in case_id['case_id']:
                # Retrieve the file associated with the case_id
                files = SocialMediaFile.objects.filter(id=case).first()
                if files:
                    case_file_url = files.case_file

                    # Extract text from the PDF
                    data = get_pdf_text(case_file_url)
                    if data:
                        # Summarize the extracted text
                        summary = summarize_data(data)
                        
                        # Generate category prompt based on the summary
                        generated_data = generate_category_prompt(summary)
                        
                        prompt_list = generated_data.split('\n')
                   
                        indexed_prompts=[]
                        for prompt in prompt_list:
                        
                            indexed_prompts.append(CaseFilePrompt(case_files=files, text=prompt.strip()))

                        # Bulk create the prompts
                        created_prompts = CaseFilePrompt.objects.bulk_create(indexed_prompts)

                        serialized_prompts.extend([{'text': prompt.text, 'id': prompt.id} for prompt in created_prompts])

            return JsonResponse({'status': 'success', 'data': serialized_prompts}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'invalid request'}, status=400)




def create_media_prompt(request):
    if request.method == 'POST':
        print(request.FILES)

        user = request.user
        company = request.user.company.id
        media_file = request.FILES.get('media_file')
        serialized_prompts = []

        if not company or not media_file:
            return JsonResponse({'status': 'error', 'message': 'Company ID and media file are required'}, status=400)

        company = get_object_or_404(CompanyList, id=company)

        media_prompt = MediaPrompt(
            user=user,
            company=company,
            media_file=media_file
        )
        media_prompt.save()
        if media_prompt:
                    case_file_url = media_prompt.media_file

                    # Extract text from the PDF
                    data = get_pdf_text(case_file_url)
                    if data:
                        # Summarize the extracted text
                        summary = summarize_data(data)
                        
                        # Generate category prompt based on the summary
                        generated_data = generate_category_prompt(summary)
                        # print(generated_data,'====[[[[[generated_data]]]]]')
                        
                        prompt_list = generated_data.split('\n')
                        # print(prompt_list,'==========prompt_listprompt_list')
                   
                        indexed_prompts=[]
                        for prompt in prompt_list:
                            clean_prompt = prompt.strip()
                            # print(clean_prompt,'=======[[[[[[[[[promptprompt]]]]]]]]]')
                            if clean_prompt:  # Ensure we don't save empty prompts
                                indexed_prompts.append(CaseFilePrompt(media_prompt=media_prompt, text=clean_prompt))
                            
                            # print(1+'1')
                        
                            # indexed_prompts.append(CaseFilePrompt(media_prompt=media_prompt, text=prompt.strip()))

                        # Bulk create the prompts
                        created_prompts = CaseFilePrompt.objects.bulk_create(indexed_prompts)

                        serialized_prompts.extend([{'text': prompt.text, 'id': prompt.id} for prompt in created_prompts])

        return JsonResponse({'status': 'success', 'data': serialized_prompts}, status=200)

        # return JsonResponse({'status': 'success', 'message': 'MediaPrompt created successfully'}, status=201)

    return JsonResponse({'status': 'invalid request'}, status=400)

    # if request.method == 'POST':
    #     print(json.loads(request.body))
    #     case_id = json.loads(request.body)
    #     for case in case_id['case_id']:
    #         # Retrieve the file associated with the case_id
    #         files = SocialMediaFile.objects.filter(id=case).first()
    #         if files:
    #             case_file_url = files.case_file
    #             print(case_file_url.url)

    #             data = get_pdf_text(case_file_url)
    #             print(data,'pppppp')

    #             summarize = summarize_data(data)
    #             # print(summarize,'ppppsummarize_data')

    #             generated_data=generate_category_prompt(summarize)
    #             print(generated_data)

                


                
              
                # # Download the file from the URL
                # response = requests.get(case_file_url.url)
                # print('i am hrerer')
                # if response.status_code == 200:
                #     # Write the file content to a temporary file
                #     temp_file_path = '/tmp/temp_file.csv'  # Adjust the file extension if necessary
                #     with open(temp_file_path, 'wb') as temp_file:
                #         temp_file.write(response.content)
                    
                    # Upload the file to the desired service
                # file = client.files.create(
                #     file=open(str(case_file_url), "rb"),
                #     purpose='assistants'
                # )
                # FileObject(id='file-LEqwPab6sXq9Czl0UQZ3Yuzu', bytes=8605, created_at=1718113703, filename='temp_file.csv', object='file', purpose='assistants', status='processed', status_details=None)

                # print(file,'p----p-p-p-p-pp-p-p')

                   
                    # client = OpenAI()

                    # data = client.files.retrieve("file-LEqwPab6sXq9Czl0UQZ3Yuzu")
                    # print(data,'00000000000000000000000000')

    