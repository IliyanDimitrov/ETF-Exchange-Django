from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from .forms import TickerForm
from .tiingo import get_meta_data, get_price_data, get_data_from_api
from stockexchange import settings
from .models import Order, Balance
from decimal import Decimal
from datetime import datetime, timedelta


import uuid
import os


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
    user = request.user
    balances = Balance.objects.filter(user=user)

    # Get the current price for each ETF in the user's portfolio
    for balance in balances:
        current_price = get_price_data(balance.ticker)
        balance.current_price = round(Decimal(current_price['close']), 2)

        # Calculate the PnL for each ETF
        balance.pnl = (balance.current_price - balance.price) * balance.quantity

    context = {
        'user': user,
        'balances': balances,
    }
    return render(request, 'main/portfolio.html', context)

def etf(request):
    data = get_data_from_api()
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

#Order View
def checkout(request):
    # Retrieve the order details from the database
    #orders = Order.objects.filter(fulfilled=False)
    # Replace with the actual order PK
    order = Order.objects.last()  
    
    context = {
        'order': order,  # Pass the orders to the template
        'Order': Order,  # Pass the Order model to the template
        'paypal_id': settings.PAYPAL_CLIENT_ID,
    }
    return render(request, 'main/checkout.html', context)

# Order Creation
def create_order(request):
    if request.method == 'POST':
        # Get the form data
        ticker = request.POST.get('ticker')
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        type = request.POST.get('type')
        user = request.user

        # Delete any existing unfulfilled orders for the user
        Order.objects.filter(user=user, fulfilled=False).delete()

        # Create the new order
        order = Order.objects.create(
            ticker=ticker,
            name=name,
            price=price,
            quantity=quantity,
            type=type,
            user=user,
            # expiry_time=datetime.now() + timedelta(minutes=1),  # set the expiry time to 1 minute from now
        )
        return redirect('/orders/checkout/')  # Redirect to the checkout page
    else:
        # Render the form for creating an order
        return render(request, 'main/etf.html')

@require_POST
def update_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    fulfilled = request.POST.get('fulfilled', True)
    order.fulfilled = fulfilled
    order.save()
    if order.fulfilled:
        balance = Balance(
            ticker=order.ticker,
            name=order.name,
            price=order.price,
            quantity=order.quantity,
            user=order.user
        )
        balance.save()
    return HttpResponse(status=200)

@require_POST
def delete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('/orders/checkout/')  # Redirect to the checkout page

