from . import (transaction_sorter, wallet_searcher, data_manipulation,
                       cpi_stat, daily_stat_comparison)
from aggregator.apps import AggregatorConfig

import time
import json
from datetime import datetime
from sys import exit
from aggregator.models import Wallet, Aggregator
#========================PARAMETERS=============================================

search_range = AggregatorConfig.PAGE_SEARCH_RANGE
start_page = AggregatorConfig.START_PAGE
end_position = AggregatorConfig.WALLET_SEARCH_END_POSITION

# status = 0 # fixes dataset error. When proper dataset implemented can be deleted


start_time = time.monotonic()

#===============================================================================

def periodic_trends():
    print("reaching server...")
    wallets = Wallet.objects.all()
    total_wallets = len(wallets)

    "Makes preliminary up to date checks for wallets before processing?????"
    wallet_searcher.main(search_range, start_page)

    wallets = Wallet.objects.all()
    total_wallets_updated = len(wallets)



    

    balance = 0
    total_delta = 0
    total_transactions_delta = 0
    total_tr_delta_all = 0
    new_wallets = total_wallets_updated - total_wallets


    for i, wallet in enumerate(wallets):
        wallet_balance = wallet.__dict__.get('balance')
        wallet_delta = wallet.__dict__.get('delta')
        wallet_transactions_delta = wallet.__dict__.get('transactions_delta')
        wallet_tr_delta_all = wallet.__dict__.get('transactions_delta_all')
        balance += float(wallet_balance)
        total_delta += float(wallet_delta)
        total_transactions_delta += int(wallet_transactions_delta)
        total_tr_delta_all += int(wallet_tr_delta_all)

    Aggregator(balance=balance,
               delta=total_delta,
               transactions_delta=total_transactions_delta,
               new_wallets=new_wallets,
               transactions_delta_all=total_tr_delta_all
               ).save()


    exit(1)



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
#!!  - send email maybe

# think about how to properly analyse data


#... write documentation for each method and proper func names
#... keep optimising, write comments, make code more pretty


# Postphoned
# maybe some interface?
# travel back in time to gain data for that date ?
# keep track of  "Addresses richer than field" ?


#Problems : polonex wallet not loading all tranasctions 17A16QmavnUfCW11DAApiJxp7ARnxN5pGX
# so only data for couple of days being used
