from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

from .models import CustomUser

from django.contrib.auth import get_user_model

from django.conf import settings

from django.core.exceptions import ValidationError

from django.forms import ModelForm

from django.contrib.auth import authenticate

from cloudinary.forms import CloudinaryFileField

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text="Required. Enter a valid email address", widget=forms.EmailInput(attrs={'placeholder' :'Email', 'style': 'width: 100%;', 'class': 'form-control'}))
    password1 = forms.CharField(max_length=64, label='Password', widget=forms.PasswordInput(attrs={'placeholder' :'Password', 'style': 'width: 100%;', 'class': 'form-control'}), help_text='')   # to remove help text from password1 field
    password2 = forms.CharField(max_length=64, label='Password', widget=forms.PasswordInput(attrs={'placeholder' :'Confrim Password', 'style': 'width: 100%;', 'class': 'form-control'}), help_text='')   # to remove help text from password1 field

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')

    # def save(self, commit = True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])
    #     if commit:
    #         user.save()
    #     return get_user_model


class EditProfileForm(ModelForm):
    profile_pic = CloudinaryFileField()
    class Meta:
        model = get_user_model()
        fields = ('profile_pic', 'first_name', 'last_name', 'phone')
        widgets = {
            'first_name': forms.TextInput (attrs={'placeholder' :'Enter your first name', 'style': 'width: 100%;', 'class': 'form-control'}),
            'last_name': forms.TextInput (attrs={'placeholder' :'Enter your last name', 'style': 'width: 100%;', 'class': 'form-control'}),
            'phone': forms.TextInput (attrs={'placeholder' :'Enter your Phone Number', 'style': 'width: 100%;', 'class': 'form-control'})
        }


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(max_length=254, help_text="Required. Enter a valid email address", widget=forms.EmailInput(attrs={'placeholder' :'Email', 'style': 'width: 100%;', 'class': 'form-control'}))
    password = forms.CharField(max_length=64, label='Password', widget=forms.PasswordInput(attrs={'placeholder' :'Password', 'style': 'width: 100%;', 'class': 'form-control'}))   # to remove help text from password1 field
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


    # username = forms.EmailField(
    #     max_length=100,
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             # "class": "block w-full px-4 py-2 mt-2 text-gray-700 placeholder-gray-500 bg-white border rounded-md bg-gray-800 border-gray-600 placeholder-gray-400 focus:border-blue-400 focus:border-blue-300 focus:ring-opacity-40 focus:outline-none focus:ring focus:ring-blue-300",
    #             "class": "form-control",
    #             "placeholder": "Username",
    #             "type": "",
    #             'style': 'width: 100%',
    #         }
    #     ),
    # )
    # password = forms.CharField(
    #     required=True,
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "class": "form-control",
    #             "type": "password",
    #             "placeholder": "Password",
    #             'style': 'width: 100%',
    #         }
    #     ),
    # )

    

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=30,help_text='Required. Inform a valid email address.', widget=forms.EmailInput(attrs={'autofocus': 'autofocus','placeholder' :'Email', 'style': 'width: 100%;', 'class': 'form-control'}))
    class Meta:
        model = get_user_model()
        fields = ("email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not get_user_model().objects.filter(email=email).exists():
            raise ValidationError("Invalid Email")
        return email  

class CustomPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=64, label='New Password', widget=forms.PasswordInput(attrs={'placeholder' :'New Password', 'style': 'width: 100%;', 'class': 'form-control'}), help_text='')   # to remove help text from password1 field
    new_password2 = forms.CharField(max_length=64, label='Confirm New Password', widget=forms.PasswordInput(attrs={'placeholder' :'Confrim Password', 'style': 'width: 100%;', 'class': 'form-control'}), help_text='')
    class Meta:
        model = get_user_model()
        # model = get_user_model()
        # get_user_model() is intended for use in reuseable Django apps, such as those you install from PyPI. Such apps cannot know what the user model class is, so they need to use get_user_model() to refer to it. Within a project, where you know what your user model class is, you can directly import django.contrib.auth.models User.
        fields = ('new_password1', 'new_password2', )