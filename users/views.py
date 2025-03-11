from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.views.generic.edit import UpdateView 
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import CustomUser
from django.shortcuts import redirect, render

from users.forms import CustomSignUpForm, CustomLoginForm, CustomPasswordResetForm, CustomPasswordResetConfirmForm, EditProfileForm


# Create your views here.



class EditUserProfileView(LoginRequiredMixin, UpdateView):
    form_class = EditProfileForm
    template_name = "registration/edit_user_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):
        """
        Returns the request's user.
        """
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile Updated Successfully')
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url
    
class ViewUserProfileView(LoginRequiredMixin, generic.DetailView):
    model = CustomUser
    template_name = "registration/view_user_profile.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user

class CustomSignUpView(generic.CreateView):
    form_class = CustomSignUpForm #We're subclassing the generic class-based view CreateView in our SignUp class. We specify using the built-in UserCreationForm
    success_url = reverse_lazy("users:edit-user-profile")
    template_name = "registration/signup.html"

    # To autologin after successful signup
    def form_valid(self, form):
        response = super(CustomSignUpView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        user = form.save()
        login(self.request, user)
        return response

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    redirect_authenticated_user: bool = True
    success_url = reverse_lazy("home")
    template_name: str = "registration/login.html"

    def form_invalid(self, form):
        print(form.errors)  # Add this line to print form errors to the console
        return self.render_to_response(self.get_context_data(form=form))

# def logout_view(request):
#     logout(request)

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    # redirect_authenticated_user: bool = True
    success_url = reverse_lazy("password_reset_done")
    template_name: str = "registration/password_reset.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    success_url = reverse_lazy("password_reset_complete")
    template_name: str = "registration/password_reset_confirm.html"