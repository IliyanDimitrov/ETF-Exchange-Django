from django.shortcuts import render

def main(request):
    return render(request, 'main/main.html', {'title': 'Main Page'})

def portfolio(request):
    return render(request, 'main/portfolio.html')

