import datetime
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
from django.contrib.auth.models import User


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


# def portfolio(request):
#     user = request.user
#     balances = Balance.objects.filter(user=user)

#     # Check if there are any unfulfilled orders
#     if Order.objects.filter(user=user, fulfilled=False).exists():
#         Order.objects.filter(user=user, fulfilled=False).delete()

#     #PnL model fields
#     principal = 0    
#     total_pnl = 0
#     # Get the current price for each ETF in the user's portfolio
#     for balance in balances:
#         current_price = get_price_data(balance.ticker)
#         balance.current_price = round(Decimal(current_price['close']), 2)

#         # Calculate the PnL for each ETF
#         balance.pnl = (balance.current_price - balance.buy_price) * balance.quantity
#         # Sum total Pnl
#         total_pnl += balance.pnl
#         principal += balance.buy_price * balance.quantity
#         # Save the total PnL for the user's portfolio
#         portfolio_pnl = PortfolioPnL(user=user, pnl=total_pnl, principal=principal)
#         portfolio_pnl.save()
   

#     context = {
#         'user': user,
#         'balances': balances,
#         'total_pnl': total_pnl,
#         'principal': principal,
#     }
#     return render(request, 'main/portfolio.html', context)
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

    context = {
        'user': user,
        'balances': balances,
        'total_pnl': total_pnl,
        'principal': principal,
    }
    return render(request, 'main/portfolio.html', context)
# def update_portfolio_pnl():
#     # Get all users
#     users = User.objects.all()

#     # Calculate and save the PnL for each user's portfolio
#     for user in users:
#         balances = Balance.objects.filter(user=user)
#         total_pnl = 0
#         principal = 0

#         # Calculate the PnL for each ETF in the user's portfolio
#         for balance in balances:
#             current_price = get_price_data(balance.ticker)
#             balance.current_price = round(Decimal(current_price['close']), 2)
#             balance.pnl = (balance.current_price - balance.buy_price) * balance.quantity
#             total_pnl += balance.pnl
#             principal += balance.buy_price * balance.quantity

#         # Save the total PnL for the user's portfolio
#         portfolio_pnl = PortfolioPnL(user=user, pnl=total_pnl, principal=principal)
#         portfolio_pnl.save()

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

