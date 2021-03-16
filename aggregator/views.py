from django.shortcuts import render, redirect # transforms templates to HttpResponse
from django.http import HttpResponse
from .models import Wallet, Aggregator
from .utils import analyse, wallet_categories, ploting
from .tests import sorter
# Create your views here.
#Views always has to return HttpResponse or exceptions

# def home(request): # must take request
#     return HttpResponse("<h1>test</h1>")
#
#
# def about(request):
#     return HttpResponse("<h1><u>About</u></h1>")

def tests(request):
    sorter()
    return render(request, 'aggregator/home.html')


def home(request): # must take request
    # passed variables have to be dict?
    wallets = {
        'wallets' :  Aggregator.objects.all()
    }

    return render(request, 'aggregator/home.html', wallets)


def about(request):
    # passing dictionary as argument so that page has a title
    return render(request, 'aggregator/about.html', {'title': 'about'})


def agg_func(request):
    analyse.periodic_trends()
    wallets = {
        'wallets' :  Aggregator.objects.all()

    }

    return render(request, 'aggregator/home.html', wallets)



def cat_func(request):
    wallet_categories.cat_sorter()
    wallets = {
        'wallets' :  Aggregator.objects.all()

    }

    return render(request, 'aggregator/home.html', wallets)








def light_theme(request):
    theme = {'type': 'light'}
    return render(request, 'aggregator/plot.html', theme)



def dark_theme(request):
    theme = {'type': 'dark'}
    return render(request, 'aggregator/plot_dark.html',theme)


    # theme = request.POST
    # print(theme )

    # return redirect(plot_func)
    # return redirect(plot_func)


def plot_func(request):
    "Desctiption"
    #
    #
    # plot = ploting.agg_plot()

    for x in range(0,2):
        # print(x)

        ploting.Main_Plot_Maker.plot_style  = 'dark_background'
        if x == 1:
            ploting.Main_Plot_Maker.plot_style  = 'Solarize_Light2'
            # ploting.Main_Plot_Maker.change_style('ggplot')

        all_plot = ploting.Main_Plot_Maker('b', 'All wallet aggregation', 'all')
        algo_plot = ploting.Main_Plot_Maker('m', 'High-volume wallet aggregation', 'algo') #_balance', 'algo_delta_per')
        exchanges_plot = ploting.Main_Plot_Maker('y', 'Exhanges wallet aggregation', 'exchanges')
        trading_plot = ploting.Main_Plot_Maker('c', 'Medium-volume wallet aggregation', 'trading') #_balance', 'algo_delta_per')
        marked_plot = ploting.Main_Plot_Maker('r', 'Interesting wallet aggregation', 'marked')

        combined_plot = ploting.Main_Plot_Maker('b', 'Categories wallet aggregation')



        all_plot.plot_type1(['aggregation_date', 'balance', 'delta_per'])
        all_plot.plot_type1(['aggregation_date', 'balance', 'btc_price'], 'Balance (BTC)',
                    'all_btc', 'Wallet aggregation and BTC price', 'BTC price ($)')
        all_plot.plot_type1(['aggregation_date', 'transactions_delta', 'btc_price'],
                                'Transactions delta','tr_delta_btc_price',
                                'Transactions delta and BTC price', 'BTC price ($)')
        all_plot.plot_type1(['aggregation_date', 'new_wallets', 'btc_price'],
                                'New wallets','new_wallets_btc_price',
                                'Daily new wallets and BTC price', 'BTC price ($)')

        algo_plot.plot_type1(['aggregation_date', 'algo_balance', 'algo_delta_per'])
        exchanges_plot.plot_type1(['aggregation_date', 'exchanges_balance', 'exchanges_delta_per'])
        trading_plot.plot_type1(['aggregation_date', 'trading_balance', 'trading_delta_per'])
        marked_plot.plot_type1(['aggregation_date', 'marked_balance', 'marked_delta_per'])


        combined_plot.plot_type2('all', 'algo', 'exchanges', 'trading', 'marked')

        ploting.Main_Plot_Maker.plot_type3()
        ploting.Main_Plot_Maker.plot_type4()
        ploting.Main_Plot_Maker.plot_type5()
        ploting.Main_Plot_Maker.plot_type6()
        ploting.Main_Plot_Maker.plot_type7()
    # print(algo_plot.name)
    # ploting.algo_plot.plot_cat

    return render(request, 'aggregator/plot.html')
    return redirect(home)























def wallets_list(request):
    "Desctiption"
    from datetime import datetime, timedelta
    from django.utils import timezone
    wallet_list = []
    new_wallet_list = []
    db_wallets = Wallet.objects.values() #.order_by('balance')
    today_date = timezone.now()
    # Author.objects.order_by('-score', 'last_name')[:30]
    # db_wallets = {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    for wallet in db_wallets:
        if timedelta(hours = 24) > today_date - wallet.get('updated_at'):
            wallet_list.append(wallet)

    # wallets = Wallet.objects.values() #.order_by('balance')
    wallet_list = sorted(wallet_list, key=lambda k: float(k['balance']), reverse=True)
    for i, wallet in enumerate(wallet_list):
        # print(x)
        new_wallet_list.append([i+1, wallet.get('address'), round(float(wallet.get('balance'))),
                               wallet.get('in_nums'), wallet.get('out_nums')]

        )

    wallets = {
        'wallets' :  new_wallet_list,
        'date' : str(today_date)[:10],
    }


    return render(request, 'aggregator/wallets.html', wallets)
