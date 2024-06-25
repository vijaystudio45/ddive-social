
from django import forms
from .models import CustomUser, CompanyList







class CreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    role = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    company_list_id = forms.ModelChoiceField(queryset=CompanyList.objects.all(), empty_label="(Select Company)", required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data
    



class CustomUserCreationForm(CreateUserForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'company', 'company_name', 'groups', 'user_permissions')