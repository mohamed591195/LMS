from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from users.models import SysUser


class Register(UserCreationForm):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('a user with this email is already registered')
        return email

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = SysUser
        fields = ['personal_image']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class SearchUsersForm(forms.Form):
    user = forms.CharField(required=False)
    user.widget.attrs.update(placeholder='search with email, username, first or second name ')