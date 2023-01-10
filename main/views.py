from datetime import datetime
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseRedirect
from .forms import TickerForm
from .tiingo import get_meta_data, get_price_data, get_data_from_api
from stockexchange import settings
from .models import Order, Balance, PortfolioPnL
from decimal import Decimal


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

    # Check if there are any unfulfilled orders
    if Order.objects.filter(user=user, fulfilled=False).exists():
        Order.objects.filter(user=user, fulfilled=False).delete()

    # Get the latest PnL values from the PortfolioPnL model
    portfolio_pnl = PortfolioPnL.objects.filter(user=user).latest('date')
    total_pnl = portfolio_pnl.pnl
    principal = portfolio_pnl.principal

    # Get the current price for each ETF in the user's portfolio
    for balance in balances:
        current_price = get_price_data(balance.ticker)
        balance.current_price = round(Decimal(current_price['close']), 2)
        # Calculate the PnL for each ETF
        balance.pnl = (balance.current_price - balance.buy_price) * balance.quantity

    # Get the PnL data from the PortfolioPnL model
    pnl_data = PortfolioPnL.objects.filter(user=user).values('date', 'pnl')
    # Convert the PnL data to a list of dictionaries
    pnl_data_list = list(pnl_data)

    # Convert the date objects in the PnL data to strings
    for item in pnl_data_list:
        item['date'] = item['date'].strftime('%Y-%m-%d')

    # Convert the PnL data to a JSON object
    pnl_data_json = json.dumps([{'pnl': str(p['pnl']), 
                                'date': datetime.strptime(p['date'], '%Y-%m-%d').
                                strftime('%Y-%m-%d')} for p in pnl_data])
    context = {
        'user': user,
        'balances': balances,
        'total_pnl': total_pnl,
        'principal': principal,
        'pnl_data_json': pnl_data_json
    }
    return render(request, 'main/portfolio.html', context)

# ETF page
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
        )
        return redirect('/orders/checkout/')  # Redirect to the checkout page
    else:
        # Render the form for creating an order
        return render(request, 'main/etf.html')

@require_POST
def update_order_and_balance(request, pk):
    order = get_object_or_404(Order, pk=pk)
    fulfilled = request.POST.get('fulfilled', True)
    order.fulfilled = fulfilled
    order.fulfilled_date = datetime.datetime.now()
    order.save()
    try:
        # after the order is fulfiled the etf balance is updated and saved
        balance = Balance.objects.get(ticker=order.ticker, user=order.user)
        balance.quantity += order.quantity
        balance.buy_price = (balance.buy_price *
                             balance.quantity + 
                             order.price * 
                             order.quantity) / (balance.quantity + order.quantity)
        balance.save()
        # if there is no balance for the particular etf, new record is created
    except Balance.DoesNotExist:
        balance = Balance(
            ticker=order.ticker,
            name=order.name,
            buy_price=order.price,
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

