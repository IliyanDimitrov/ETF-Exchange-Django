from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from stockexchange import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
# from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Function to check if the user is a client
def is_client(user):
    if user.is_staff or user.is_superuser:
        return False
    else:
        return True

def register(request):
    #Making sure the user cannot access registeration page if logged in
    if request.user.is_authenticated is True:
        return render(request, 'users/profile.html')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        form_email = form['email'].value()
        existing_users = User.objects.filter(email=form_email)

        # Existing Email Check
        if existing_users.count():
            messages.warning(request, f'Email has been used already!')
            form = UserRegisterForm()
            return render(request, 'users/register.html', {'form': form})

        # Validate form input and remove user admin priviliges
        if form.is_valid():
            user = form.save()
            # default to non-active
            user.is_active = False
            user.is_staff = False
            user.is_superuser = False
            user.save()

            #Email details
            uid = urlsafe_base64_encode(force_bytes(User.objects.last().pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            name = User.objects.last().first_name

            # Site account creation message.
            messages.success(
                request, f'Your account has been created. Please confirm your email to finish your registration!')

            # Welcome Email Setup
            subject = 'Welcome to ETF Exchange'
            message = "Thanks for having us. Please confirm your email to finish your registration!"
            sender = settings.EMAIL_HOST_USER
            receiver = User.objects.last().email
            password = settings.EMAIL_HOST_PASSWORD

            # Welcome Email Dispatch
            send_mail(subject, message, sender, [receiver], fail_silently=False, auth_password=password)

            # Confiramation Email Setup
            email_subject = "Confirm your Email @ ETF Exchange"
            message2 = render_to_string('users/confirmation_email.html', {
                'name': user.first_name,
                'domain': domain,
                'uid': uid,
                'token': generate_token.make_token(user)
            })

            # Confiramation Email Setup
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [receiver],
            )
            # Confiramation Email Dispatch
            email.fail_silently = True
            email.send()
            return redirect('two_factor:login')
    else:
        #Error message and registration form reset
        messages.warning(
                     request, f'Error please try again!')
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})


@login_required
@user_passes_test(is_client)
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
        request.FILES, 
        instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request, f'Your account has been updated.')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    

    context = {
       'u_form': u_form,
       'p_form': p_form, 
    }
    return render(request, 'users/profile.html', context)

@login_required
@user_passes_test(is_client)
def portfolio(request):
    return render(request, 'main/portfolio.html')

def activate(request, uidb64, token):
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        messages.success(
                request, f'Your account has been created. Please confirm your email to finish your registration!')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    
    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your Account has been activated!!")
        return redirect('two_factor:login')
        
    else:
        return render(request, 'users/activation_failed.html')

