from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

# Function to check if the user is a client
def is_client(user):
    if user.is_staff or user.is_superuser:
        return False
    else:
        return True

def main(request):
    return render(request, 'main/main.html', {'title': 'Main Page'})

@login_required
@user_passes_test(is_client)
def portfolio(request):
    return render(request, 'main/portfolio.html')

