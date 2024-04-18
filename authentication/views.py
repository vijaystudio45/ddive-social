from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from authentication.models import CustomUser as User
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
from social_media_post.models import UserAccessToken
from authentication.permissions import admin_only
from .helper import StringEncoder






def index(request):
    return render(request, 'index.html')




def signup(request):


    if not request.user.is_superuser:
        return redirect('/')



    lists = CompanyList.objects.all()
  
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        company_list_id = request.POST.get('company_list')

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
        if company_list_id:
            company_list = CompanyList.objects.get(id=company_list_id)
            new_user.company = company_list
            new_user.save()

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
   


from .models import CompanyList

def CompanyLists(request):
    lists = CompanyList.objects.all()
    return render(request, 'signup.html', {'lists': lists})


#calender
def calenderview(request):
    return render(request,'Calendar.html')




##########------------------------------############
from social_media_post.models import GeneratePost



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
    if response.status_code == 200:
        
        print("Successfully logged out from LinkedIn")
        # Redirect the user regardless of the result of the API call
        return redirect('/')

    