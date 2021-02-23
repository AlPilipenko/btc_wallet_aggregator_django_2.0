from django.shortcuts import render # transforms templates to HttpResponse
from django.http import HttpResponse
from .models import Wallet
from .utils import analyse
# Create your views here.
#Views always has to return HttpResponse or exceptions

# def home(request): # must take request
#     return HttpResponse("<h1>test</h1>")
#
#
# def about(request):
#     return HttpResponse("<h1><u>About</u></h1>")


def home(request): # must take request
    # passed variables have to be dict?
    wallets = {
        'wallets' : Wallet.objects.all()
    }

    return render(request, 'aggregator/home.html', wallets)


def about(request):
    # passing dictionary as argument so that page has a title
    return render(request, 'aggregator/about.html', {'title': 'about'})


def agg_func(request):
    analyse.periodic_trends()
    wallets = {
        'wallets' : Wallet.objects.all()

    }

    return render(request, 'aggregator/home.html', wallets)