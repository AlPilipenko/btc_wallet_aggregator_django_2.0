from . import wallet_searcher, wallet_categories, wallet_list_maker, ploting
from aggregator.apps import AggregatorConfig

import time
import json
from datetime import datetime
from sys import exit
from aggregator.models import Wallet, Aggregator, Category, Wallet_List
#========================PARAMETERS=============================================

search_range = AggregatorConfig.PAGE_SEARCH_RANGE
start_page = AggregatorConfig.START_PAGE
end_position = AggregatorConfig.WALLET_SEARCH_END_POSITION

#===============================================================================
def percentage_diff(new_value, old_value):
    try:
        diff = round(((new_value - old_value) / old_value) * 100, 2)
        return diff
    except:
        return 0


def cat_trends_calc(category, wallets_scraped_list, cat_name):
    "Aggregates balances of wallets by categories"
    balance = 0
    total_delta = 0
    last_record = Category.objects.last()

    for wallet in category:
        wallet_name = wallet.__dict__.get('wallet_name')

        if str(wallets_scraped_list).find(wallet_name) == -1:
            continue

        wallet_balance = wallet.__dict__.get('balance')
        print(cat_name, wallet_name, wallet_balance )
        # wallet_delta = wallet.__dict__.get('delta')
        balance += float(wallet_balance)

    if last_record != None:
        old_balance = last_record.__dict__.get(cat_name+'_balance')
        delta_per = percentage_diff(balance, float(old_balance))
        total_delta = balance - float(old_balance)
    else:
        delta_per = 0
        total_delta = 0
    return round(balance), round(total_delta), delta_per


def all_trends_calc(wallets ,wallets_scraped_list):
    "Aggregates balances of all wallets"
    balance = 0
    delta = 0
    real_delta = 0
    tr_delta = 0
    tr_delta_all = 0
    last_record = Aggregator.objects.last()

    for i, wallet in enumerate(wallets):
        wallet_name = wallet.__dict__.get('wallet_name')
        if str(wallets_scraped_list).find(wallet_name) == -1:
            continue
        wallet_balance = wallet.__dict__.get('balance')
        wallet_transactions_delta = wallet.__dict__.get('transactions_delta')
        wallet_tr_delta_all = wallet.__dict__.get('transactions_delta_all')
        balance += float(wallet_balance)
        tr_delta += int(wallet_transactions_delta)
        tr_delta_all += int(wallet_tr_delta_all)

        "testing this"
        real_wallet_delta = wallet.__dict__.get('delta')
        real_delta += float(real_wallet_delta)

    if last_record != None:
        old_balance = last_record.__dict__.get('balance')
        delta_per = percentage_diff(balance, float(old_balance))
        "balance delta"
        delta = balance - float(old_balance)
    else:
        delta_per = 0
        delta = 0
    return (round(balance), round(delta), round(real_delta),
                                              tr_delta, tr_delta_all, delta_per)


def plot_func():
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
        all_plot.plot_graph_type1(['aggregation_date','new_wallets','btc_price'],
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


def periodic_trends():
    start_time = time.monotonic()
    "Aggregates balances of the most rich BTC wallets"
    print("reaching server...")
    wallets = Wallet.objects.all()
    total_wallets = len(wallets)

    "Updates database"
    print("Updating database")
    wallets_scraped_list, btc_price = wallet_searcher.main(search_range, start_page)
    "Depending on wallet performance designates it to particular category"
    print("Allocating wallets to categories")
    wallet_categories.cat_sorter()


    #=========================== for debug======================================
    # btc_price = 60456
    # import ast
    # db_string_list =  Wallet_List.objects.first().wallet_list
    # wallets_scraped_list = ast.literal_eval(db_string_list)

    #===========================================================================

    wallets = Wallet.objects.all()
    total_wallets_updated = len(wallets)
    new_wallets = total_wallets_updated - total_wallets
    bal, delta, tr_delta, real_delta ,tr_delta_all, delta_per = all_trends_calc(
                                                wallets, wallets_scraped_list)

    Aggregator(balance=bal,
               delta=delta,
               real_delta=real_delta,
               delta_per=delta_per,
               transactions_delta=tr_delta,
               transactions_delta_all=tr_delta_all,
               new_wallets=new_wallets,
               btc_price=btc_price,
               ).save()


    marked = Wallet.objects.filter(category='marked').all()
    exchanges = Wallet.objects.filter(category='exchange/pool').all()
    algo = Wallet.objects.filter(category='algo').all()
    trading = Wallet.objects.filter(category='trading').all()

    marked_bal, marked_delta, marked_delta_per = cat_trends_calc(marked,
                                                 wallets_scraped_list, 'marked')
    ex_bal, ex_delta, ex_delta_per = cat_trends_calc(exchanges,
                                              wallets_scraped_list, 'exchanges')
    algo_bal, algo_delta, algo_delta_per = cat_trends_calc(algo,
                                                    wallets_scraped_list,'algo')
    trade_bal, trade_delta, trade_delta_per = cat_trends_calc(trading,
                                                wallets_scraped_list, 'trading')

    Category(marked_balance=marked_bal,
             marked_delta=marked_delta,
             marked_delta_per=marked_delta_per,
             exchanges_balance=ex_bal,
             exchanges_delta=ex_delta,
             exchanges_delta_per=ex_delta_per,
             algo_balance=algo_bal,
             algo_delta=algo_delta,
             algo_delta_per=algo_delta_per,
             trading_balance=trade_bal,
             trading_delta=trade_delta,
             trading_delta_per=trade_delta_per,
            ).save()

    print("Making a list of todays wallets")
    wallet_list_maker.wallet_list_maker_func()
    print("Making today's plots")
    plot_func()
    print(f'Time passed ~{round((time.monotonic() - start_time)/60,2)},minutes')
