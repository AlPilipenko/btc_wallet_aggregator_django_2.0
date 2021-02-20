from . import (transaction_sorter, wallet_searcher, data_manipulation,
                       cpi_stat, daily_stat_comparison)
from aggregator.apps import AggregatorConfig
from progressbar import ProgressBar
import time
import json
from datetime import datetime
from sys import exit
from aggregator.models import Wallet
#========================PARAMETERS=============================================

search_range = AggregatorConfig.PAGE_SEARCH_RANGE
start_page = AggregatorConfig.START_PAGE
end_position = AggregatorConfig.WALLET_SEARCH_END_POSITION

# status = 0 # fixes dataset error. When proper dataset implemented can be deleted

bar = ProgressBar(maxval = 100)
start_time = time.monotonic()

#===============================================================================

def periodic_trends():

    print("reaching server...")





    "Makes preliminary up to date checks for wallets before processing"
    wallet_searcher.main(search_range, start_page)


    # print(wallet_addresses)
    wallets = Wallet.objects.all()
    wallets_to_analyse = Wallet.objects.filter(up_to_date='no').all()
    db_wallets = Wallet.objects.filter(up_to_date='yes').all()
    # print(wallets_to_analyse)



    complete_values_table = []
    #print(len(wallet_addresses))
    #print(wallet_addresses)
    #n = 1
    day = 0
    week = 0
    month = 0
    quarter = 0
    half_year = 0
    year = 0
    two_years = 0
    three_years = 0
    five_years = 0
    all_time = 0

    for i, wallet in enumerate(wallets[:end_position]):
        time.sleep(5)
        bar.start()
        bar_index = len(wallets[:end_position]) / 100
        bar.update(i/bar_index)

        print(i, wallet.__dict__.get('address'))


        up_to_date = wallet.__dict__.get('up_to_date')
        address = wallet.__dict__.get('address')
        in_transactions = wallet.__dict__.get('in_nums')
        out_transactions = wallet.__dict__.get('out_nums')


        try:
            total_transactions = int(in_transactions) + int(out_transactions)
        except ValueError:
            total_transactions = 0


        if up_to_date == 'no':
            if total_transactions > 50000:
                url = 'https://bitinfocharts.com/bitcoin/address/' + address
            else:
                url = 'https://bitinfocharts.com/bitcoin/address/' + address + '-full'
            wallets_trans_delta = transaction_sorter.values_extractor(url, address)


###############################################
        # complete_data = [v[0],v[1], wallets_trans_delta[:7], round(wallets_trans_delta[-1]), v[2]]
        #
        # if complete_data == None:
        #     print("fixing dataset error")
        #     debug_01.debug_dataset_error()
        #     status = 1
        #     break
        #
        # "Marks >500 wallets if >500 transactions and no token"
        # if  complete_data[3] > 500 and complete_data[1] == "None":
        #     #print("here")
        #     complete_data = list(complete_data)
        #     complete_data[1] = ">500"
        #     #complete_data = tuple(temp)
        #
        # #print(complete_data[4])
        # if complete_data[4] == '17A16QmavnUfCW11DAApiJxp7ARnxN5pGX':
        #     complete_data[2][2] = complete_data[2][3] = complete_data[2][4] = complete_data[2][5] =  complete_data[2][6] = 0
#################################################################

        # trans_delta = Wallet.objects.filter(address=address)
        # trans_delta  = [0, 0, 0, 0, -106051, -114051, 141452, 141452, 141452, 141452, 233]
        trans_delta_str = wallet.__dict__.get('transactions_delta')
        import json
        trans_delta = json.loads(trans_delta_str)
        # print("trans_delta",type(trans_delta))
        day += int(trans_delta[0])
        week += int(trans_delta[1])
        month += int(trans_delta[2])
        quarter += int(trans_delta[3])
        half_year += int(trans_delta[4])
        year += int(trans_delta[5])
        two_years += int(trans_delta[6])
        three_years += int(trans_delta[7])
        five_years += int(trans_delta[8])
        all_time += int(trans_delta[9])
        # complete_values_table.append(complete_data)

    print('day', day)
    print('week', week)
    print('month', month)
    print('quarter', quarter)
    print('half_year', half_year)
    print('year', year)
    print('two_years', two_years)
    print('three_years', three_years)
    print('five_years', five_years)
    print('all_time', all_time)


    bar.finish()
    exit(1)

    new_entries = data_manipulation.wallet_data_record(complete_values_table)
    #print(complete_data)
    daily_stat_comparison.categorising_wallets(complete_values_table)

    # cpi_stat.cpi_stat_arg() # TEMP COMMENT OUT DO TO DIVISION ERROR!

    print(new_entries)
    print(datetime.now())

    print(f'Time passed ~{round((time.monotonic() -start_time)/60,2)}, minutes')

# periodic_trends()


# if status == 1:
#     periodic_trends()





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
