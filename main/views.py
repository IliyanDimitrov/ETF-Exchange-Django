from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.http import HttpResponseRedirect
from .forms import TickerForm
from .tables import EtfTable
from .tiingo import get_meta_data, get_price_data, get_data_from_api
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

def etf(request):
    data = get_data_from_api
    return render(request, 'main/etf.html', {'data': data})

# Searching bar
def etf_search(request):
    if request.method =='POST':
        form = TickerForm(request.POST)
        if form.is_valid():
            ticker = request.POST['ticker']
            return HttpResponseRedirect(ticker)
    else:
        form = TickerForm()
        return render(request, 'main/etf_search.html', {'form': form})

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