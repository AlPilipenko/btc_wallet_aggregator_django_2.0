from django.shortcuts import render, redirect # transforms templates to HttpResponse
from django.http import HttpResponse
from .models import Wallet, Aggregator, Wallet_List
from .utils import analyse, wallet_categories, ploting
from .tests import sorter
#Views always has to return HttpResponse or exceptions
# def home(request): # must take request
#     return HttpResponse("<h1>test</h1>")
# def about(request):
#     return HttpResponse("<h1><u>About</u></h1>")


def home(request): # must take request
    # passed variables have to be dict?
    theme = str(request.GET.get('value'))
    if theme == 'light':
        return render(request, 'aggregator/home.html', {'title': 'home'})
    else:
        return render(request, 'aggregator/plot_dark.html', {'title': 'home'})


def about(request):
    # passing dictionary as argument so that page has a title
    theme = str(request.GET.get('value'))
    if theme == 'light':
        return render(request, 'aggregator/about.html', {'title': 'about'})
    else:
        return render(request, 'aggregator/about_dark.html', {'title': 'about'})


def light_theme(request):
    return render(request, 'aggregator/home.html')


def dark_theme(request):
    return render(request, 'aggregator/plot_dark.html')


def wallets_list(request):
    "Desctiption"
    import ast
    values = ast.literal_eval(request.GET.get('value'))
    wallet_number, theme = int(values[0]), values[1]
    display_list = Wallet_List.objects.filter(id=1)[0].wallet_list_display
    new_wallet_list = ast.literal_eval(display_list)
    today_date = Wallet_List.objects.filter(id=1)[0].updated_at

    wallets = {
        'wallets' :  new_wallet_list[:wallet_number],
        'date' : str(today_date)[:10],
        'length_of_list' : wallet_number,
              }
    if theme == 'light':
        return render(request, 'aggregator/wallets.html', wallets)
    else:
        return render(request, 'aggregator/wallets_dark.html', wallets)


def agg_func(request):
    analyse.periodic_trends()
    return render(request, 'aggregator/home.html')


def cat_func(request):
    wallet_categories.cat_sorter()
    return render(request, 'aggregator/home.html')


def plot_func(request):
    "Desctiption"
    styles = ['dark_background', 'Solarize_Light2']
    for style in styles:
        ploting.Main_Plot_Maker.plot_style = style

        all_plot = ploting.Main_Plot_Maker('dodgerblue',
                                                'All wallet aggregation', 'all')
        algo_plot = ploting.Main_Plot_Maker('m',
                                       'High-volume wallet aggregation', 'algo')
        exchanges_plot = ploting.Main_Plot_Maker('y',
                                     'Exhanges wallet aggregation', 'exchanges')
        trading_plot = ploting.Main_Plot_Maker('c',
                                  'Medium-volume wallet aggregation', 'trading')
        marked_plot = ploting.Main_Plot_Maker('r',
                                     'Interesting wallet aggregation', 'marked')

        combined_plot = ploting.Main_Plot_Maker('dodgerblue',
                                                'Categories wallet aggregation')


        all_plot.plot_graph_type1(['aggregation_date', 'balance', 'delta_per'])
        all_plot.plot_graph_type1(['aggregation_date', 'balance', 'btc_price'],
                 'Balance (BTC)', 'all_btc', 'Wallet aggregation and BTC price',
                                                                'BTC price ($)')
        all_plot.plot_graph_type1(['aggregation_date', 'transactions_delta',
                        'btc_price'], 'Transactions delta','tr_delta_btc_price',
                            'Transactions delta and BTC price', 'BTC price ($)')
        all_plot.plot_graph_type1(['aggregation_date', 'new_wallets', 'btc_price'],
                                          'New wallets','new_wallets_btc_price',
                             'Daily new wallets and BTC price', 'BTC price ($)')
        algo_plot.plot_graph_type1(['aggregation_date', 'algo_balance',
                                                              'algo_delta_per'])
        exchanges_plot.plot_graph_type1(['aggregation_date', 'exchanges_balance',
                                                         'exchanges_delta_per'])
        trading_plot.plot_graph_type1(['aggregation_date', 'trading_balance',
                                                           'trading_delta_per'])
        marked_plot.plot_graph_type1(['aggregation_date', 'marked_balance',
                                                            'marked_delta_per'])
        combined_plot.plot_graph_type2()
        ploting.Main_Plot_Maker.plot_scatter_type1()
        ploting.Main_Plot_Maker.plot_scatter_type2()
        ploting.Main_Plot_Maker.plot_pie_type1()
        ploting.Main_Plot_Maker.plot_pie_type2()
        ploting.Main_Plot_Maker.plot_pie_type3()
    return render(request, 'aggregator/home.html')


def wallets_list_maker_func(request):
    wallet_list = []
    new_wallet_list = []
    db_wallets = Wallet.objects.values() #.order_by('balance')
    wallet_today_list = str(Wallet_List.objects.filter(id=1)[0].wallet_list)
    from django.utils import timezone
    today_date = timezone.now()

    for wallet in db_wallets:
        wallet_name = wallet.get('wallet_name')
        if wallet_today_list.find(wallet_name) == -1:
            continue
        else:
            wallet_list.append(wallet)
    wallet_list = sorted(wallet_list, key=lambda k: float(k['balance']), reverse=True)

    for i, wallet in enumerate(wallet_list):
        new_wallet_list.append([i+1, wallet.get('address'), round(float(wallet.get('balance'))),
                               wallet.get('in_nums'), wallet.get('out_nums')])
    updated_display_list = Wallet_List.objects.filter(id=1)
    updated_display_list.update(wallet_list_display = new_wallet_list)
    return render(request, 'aggregator/home.html')
