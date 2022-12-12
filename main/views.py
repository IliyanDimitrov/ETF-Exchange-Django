from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponseRedirect
from .forms import TickerForm
from .tiingo import get_meta_data, get_price_data
from .models import Transaction

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


# Searching bar
def etf(request):
    if request.method =='POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:
        form = TickerForm()
    return render(request, 'main/etf.html', {'form': form})

#Retrieve ETF information
def ticker(request, id):
    context = {}
    context['ticker'] = id
    context['meta'] = get_meta_data(id)
    context['price'] = get_price_data(id)
    return render(request, 'main/ticker.html', context)

def transactions(request):
    transactions = Transaction.objects.all()
    context = {'transactions': transactions}
    return render(request, 'main/transactions.html', context)