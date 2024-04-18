from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("linkedin_auth/",views.LinkeInAuthentication, name = "linkedin_auth"),
    path("linkedin/callback/access/", views.LinkedInAcessToken, name = "linkedin_callback_access"),

    path('calendar/', views.calenderview, name='calendar'),

    path("facebook_auth/", views.authenticate_with_facebook, name="facebook_auth"),
    path('facebook-auth-callback/', views.facebookInAcessToken, name='facebook-auth-callback'),  

    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/confirm/<str:user_id>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('privacy-policy/', views.privacypolicy, name='privacy_policy'),
    # path('createpost/',views.CreatePost, name="createpost"),  
    # path('list/', views.ItemList, name ="list"),
    # path('update/<int:pk>/', views.update_item, name='update_item'),
    # path('delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('post-view/<int:pk>/', views.PostView, name="post-view"),
    #---------------------------------------instagram login detail---------------------------------------
    path("instagram_auth/", views.authenticate_with_instagram, name="instagram_auth"),
    path('Logout_Linkedin/', views.LogoutLinkedinUser, name='Logout_Linkedin'),
  


]