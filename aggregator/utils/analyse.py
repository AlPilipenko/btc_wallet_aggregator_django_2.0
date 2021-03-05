from . import wallet_searcher, wallet_categories
from aggregator.apps import AggregatorConfig

import time
import json
from datetime import datetime
from sys import exit
from aggregator.models import Wallet, Aggregator, Category
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
    return round(balance), round(delta), round(real_delta), tr_delta, tr_delta_all, delta_per


def periodic_trends():
    "Aggregates balances of the most rich BTC wallets"
    print("reaching server...")
    wallets = Wallet.objects.all()
    total_wallets = len(wallets)

    "Updates database"
    wallets_scraped_list = wallet_searcher.main(search_range, start_page)
    "Depending on wallet performance designates it to particular category"
    wallet_categories.cat_sorter()

    #
    # wallets_scraped_list = [
    # ['200', '1FtHBKrYkDchMA1pwRTpYZ77TpfwSgh6iF', '1,000 BTC ($386,807,422 USD)', '0.04293%', '2018-12-06 05:10:20 UTC', '2021-01-22 09:36:26 UTC', '93', '', '', '2'],
    # ['200', '1FtHBKrYkDchMA1pwRTpfesf7TpfwSgh6iF', '1,000 BTC ($386,807,422 USD)', '0.04293%', '2018-12-06 05:10:20 UTC', '2021-01-22 09:36:26 UTC', '92', '', '', '1'],
    # ['200', '1FtHBKrYkDchMeaaA1pwRTpfesf7TpfwSgh6iF', '500 BTC ($386,807,422 USD)', '0.04293%', '2018-12-06 05:10:20 UTC', '2021-01-22 09:36:26 UTC', '92', '', '', '2'],
    # ['200', '1FtHBKrYkDchMA1pwRTafaafpfesf7TpfwSgh6iF', '1,000 BTC ($386,807,422 USD)', '0.04293%', '2018-12-06 05:10:20 UTC', '2021-01-22 09:36:26 UTC', '92', '', '', '2'],
    # ['200', '1FtHBKrYkDchMA1pwRTafaafpfesf7sfesefTpfwSgh6iF', '1,000 BTC ($386,807,422 USD)', '0.04293%', '2018-12-06 05:10:20 UTC', '2021-01-22 09:36:26 UTC', '93', '', '', '3'],
    # ['200', '1FtHBKrYkDchMA1pwRTafaafpfesf7sfesefTpawdfwSgh6iF', '4,000 BTC ($386,807,422 USD)', '0.04293%', '2018-12-06 05:10:20 UTC', '2021-01-22 09:36:26 UTC', '93', '', '', '4'],
    # ['200', '1FtHBKrYkDchMA1pwRTafaafpfesf7sfesefTpfeawdfwSgh6iF', '3,000 BTC ($386,807,422 USD)', '0.04293%', '2018-12-06 05:10:20 UTC', '2021-01-22 09:36:26 UTC', '93', '', '', '5'],
    # ['200', '1FtHBKrYkDchsefMA1pwRTafaafpfesf7sfesefTpfeawdfwSgh6iF', '10,000 BTC ($386,807,422 USD)', '0.04293%', '2018-12-06 05:10:20 UTC', '2021-01-22 09:36:26 UTC', '1', '', '', '']
    # ]





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



    # exit(1)



######################################################




#DONE print(len(my_table)) if more then 100 transaction, only use float
#ONLY MANUALY CHECKED check calculations of transaction using unit testing
#DONE count data to see dayly/ montly trends + simple analysing
#DONE status bar
#DONE include amount of transactions
#Done make it work for 10000 wallets
#Done(Failed yo increase process speed) Get the data quicklt first, then go through it
#Done(All variables in one page)

#Done evaluate wallets(old, robot, exchange...)
#Done --- old_wallets index error, wallet_name + lots trans = robot,
#Done --- lots trans and exchange_name = exchange, else = None

#Done find a way to extract info to file or somewhere to store

#Done make it work in such way that it doesnt need to extract full table of values every time.
#Done---Get Their number of transactions, Make dict with wallets + transactions + save to doc
#Done ---Get list of wallets first, compare to previus recorded data.
# Done   then Send for scraping only new wallets and wallets with new transactions
# Done   finally, obtain data from privios day, and display all.
# Done Double check daily percantege calculations statistics
#Done  - added percentages as day to day change of data
#Done  store daily statistics

#Done/testing how many new appearing wallets
#Done/testing Fix error when wall_tran has wallet info and dataset don't
###########################################################################################

#!! - make it daily stat readable and convinient
# !!!All data neatly presented in spreadsheet
#!! think about cpi type index solution for stats



#!! automate whole proccess

# think about how to properly analyse data


#... write documentation for each method and proper func names
#... keep optimising, write comments, make code more pretty


# Postphoned
# maybe some interface?

# keep track of  "Addresses richer than field" ?



# so only data for couple of days being used
