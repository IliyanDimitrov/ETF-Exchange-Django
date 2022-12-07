from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from stockexchange import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token

def register(request):
    #Making sure the user cannot access registeration page if logged in
    if request.user.is_authenticated is True:
        return render(request, 'users/profile.html')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # default to non-active
            user.is_active = False
            user.is_staff = False
            user.save()

            #Email details
            uid = urlsafe_base64_encode(force_bytes(User.objects.last().pk))
            current_site = get_current_site(request)
            domain = current_site.domain
            name = User.objects.last().first_name
            # Site account creation message.
            messages.success(
                request, f'Your account has been created. Please confirm your email to finish your registration!')
            # Welcome Email
            subject = 'Welcome to ETF Exchange'
            message = "Thanks for having us. Please confirm your email to finish your registration!"
            sender = settings.EMAIL_HOST_USER
            receiver = User.objects.last().email
            password =settings.EMAIL_HOST_PASSWORD
            send_mail(subject, message, sender, [receiver], fail_silently=False, auth_password=password)
            # Confiramation Email
            email_subject = "Confirm your Email @ ETF Exchange"
            message2 = render_to_string('users/confirmation_email.html', {
                'name': user.first_name,
                'domain': domain,
                'uid': uid,
                'token': generate_token.make_token(user)
            })

            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [receiver],
            )

            email.fail_silently = True
            email.send()
            return redirect('two_factor:login')

    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
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