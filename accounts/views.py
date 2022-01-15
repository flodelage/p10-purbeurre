
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q

from accounts.models import Profile
from catalog.models import Favorite
from .forms import ProfileCreationForm


def signup(request):
    """
    Allow a user to register an account
    """
    signup_form = ProfileCreationForm()
    if request.method == 'POST':
        signup_form = ProfileCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'accounts/registration/signup.html',
                  context = {'signup_form': signup_form})


def log_in(request):
    """
    Allow a user to log in
    """
    auth_form = AuthenticationForm()
    if request.method == 'POST':
        auth_form = AuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            user = authenticate(
                username=auth_form.cleaned_data['username'],
                password=auth_form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        auth_form = AuthenticationForm()
    return render(request, 'accounts/registration/login.html',
                  context = {'auth_form': auth_form})


@login_required
def log_out(request):
    """
    Allow a logged in user to log out
    """
    logout(request)
    return redirect(settings.LOGIN_REDIRECT_URL)


@login_required
def account(request):
    """
    Allow a logged in user to access to his profile details
    """
    profile = request.user
    return render(request, 'accounts/account.html',
                  context = {'profile': profile, })


@login_required
def favorites_list(request):
    """
    Allow a logged in user to see his profile details
    """
    profile = request.user
    favorites = profile.favorite_set.all()
    return render(request, 'accounts/favorites_list.html',
                  context = {'profile': profile,
                             'favorites': favorites, })


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_profiles = Profile.objects.filter(Q(email=data))
			if associated_profiles:
				for profile in associated_profiles:
					subject = "Password Reset Requested"
					email_template_name = "accounts/password/password_reset_email.txt"
					c = {
					"email":profile.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(profile.pk)),
					"profile": profile,
					'token': default_token_generator.make_token(profile),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [profile.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')

					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request, "accounts/password/password_reset.html", {"password_reset_form":password_reset_form})


@login_required
def favorite_detail(request, favorite_pk):
    """
    Allow a logged in user to see a favorite details
    """
    favorite = get_object_or_404(Favorite, id=favorite_pk)
    return render(request, 'accounts/favorite_detail.html',
                  context = {'favorite': favorite, })


@login_required
def delete_favorite(request, favorite_pk):
    """
    Allow a logged in user to delete one favorite
    """
    favorite = get_object_or_404(Favorite, id=favorite_pk)
    if request.method == 'POST':
        favorite.delete()
        messages.success(
            request, f""""{favorite.substitute.name}" a bien été supprimé"""
        )
    return redirect('favorites')
