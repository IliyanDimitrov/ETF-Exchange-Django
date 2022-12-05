from django.shortcuts import render

users = [
    {
        'name': "Iliyan Dimitrov",
        'address': "1 Uni Street, Bolton, BL1 1AA",
    }
]


def main(request):
    
    return render(request, 'main/main.html', {'title': 'Main Page'})

def portfolio(request):
    context = {
        'users': users,
    }
    return render(request, 'main/portfolio.html', context)

