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
    
    path('company-create/', views.company_create, name="company-create"),
    path('company/edit/<int:company_id>/', views.company_edit, name='company_edit'),
    path('company-details/',views.Companyalldetails,name='Company-details'),
    # path('team-member/<int:pk>/edit/', views.team_member_edit, name='team_member_edit'),
    # path('team-member/<int:pk>/delete/', views.team_member_delete, name='team_member_delete'),
    path('detail/<slug:company_name>/', views.company_detail, name='company_detail'),
    path('company_all_details/<slug:company_name>/',views.company_all_details,name='company_all_details'),
    path('team_member_list/', views.team_member_list, name='team_member_list'),
    path('team_member_add/', views.team_member_add, name='team_member_add'),
    path('team-member/<int:pk>/', views.team_member_edit, name='team_member_edit'),
    # path('team-member/edit/<int:pk>/', views.team_member_edit, name='team_member_edit'),
    path('team-member/delete/<int:pk>/', views.team_member_delete, name='team_member_delete'),
    path('team_member_list/<int:pk>/',views.get_particular_member,name='get_particular_member'),
    path('generate-prompt/',views.generate_prompt,name='generate-prompt'),
    path('static-prompts/',views.StaticPromptdata,name='static-prompt'),
    path('social_media_post/', views.social_media_post,name='social_media_post'),
    path('edit-social-media-post/<int:post_id>/', views.edit_social_media_post, name='edit_social_media_post'),


    path('get_unique_prompts/',views.get_unique_prompts, name='get_unique_prompts'),
    path('book-slot/',views.book_slot,name='book_slot'),
    path('category-list/',views.category_list,name='category-list'),
    path(
        "create-checkout-session",
        views.CreateStripeCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path("success/", views.SuccessView.as_view(), name="success"),
    path("cancel/", views.CancelView.as_view(), name="cancel"),
    path('check-voucher/', views.check_voucher_code, name='check_voucher'),
    path('voucher/', views.voucher_page, name='voucher'),
    path('case-file-data/',views.generatedfilesdata,name='case-file-data'),
    path('media-prompt/',views.create_media_prompt,name='media-prompt')




]