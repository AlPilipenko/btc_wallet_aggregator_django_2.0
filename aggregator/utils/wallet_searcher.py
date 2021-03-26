from django.db import models
from django.utils import timezone
from datetime import datetime
from aggregator.models import Wallet, Wallet_List
from random import randint
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from django.utils import timezone
from . import analyse
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

def restart_analyse():
    print("Error occured. Will try again in 1 hour")
    time.sleep(3600)
    analyse.periodic_trends()


def address_filter(wallet):
    "Extracts clean btc wallet address and gets the tag(if there is one)"
    temp = wallet


    while wallet.find('wallet') != -1:
        wallet_word = wallet.find('wallet')
        wallet = wallet[:wallet_word]

    for i, l in enumerate(wallet):
        if l == ':' or l == ' ':
            wallet = wallet[:i]
            cut = len(wallet)
            tag = temp[cut+1:]
            return wallet, tag

    while wallet.find('.') != -1:
        wallet = wallet.replace('.', '')
        cut = len(wallet)
        tag = temp[cut+1:]
        tag = '' if len(tag) == 1 else tag
        return wallet, tag

    cut = len(wallet)
    tag = temp[cut:]
    tag = '' if len(tag) == 1 else tag
    return wallet, tag


def balance_filter(balance):
    "Strips unnessecery symbols"
    cut = balance.find('BTC')
    balance = balance[:cut-1]
    balance = balance.replace(',', '')
    return balance


def date_filter(date):
    "Strips unnessecery symbols"
    cut = date.find('UTC')
    return date[:cut-1]


def wallet_sets_url_list_maker(srch_rng, start_pg):
    "Makes a URL list where from extract wallet's data (100 wallets per URL)"

    for n in range(srch_rng[0], srch_rng[1]):
        hundred_wallet_urls = f'https://bitinfocharts.com/top-100-richest-bitcoin-addresses-{start_pg}.html'
        yield hundred_wallet_urls
        start_pg += 1


def btc_price_extractor():
    "Gets current btc $ price"
    btc_price_url = f'https://bitinfocharts.com/bitcoin/'
    page = requests.get(btc_price_url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    btc_price_raw = soup.find(id="tdid2")
    btc_price = soup.select_one("span[itemprop*=price]").text.replace(',','')
    btc_price = round(float(btc_price))
    return btc_price


def wallet_data_scraper(url_list_of_sets):
    """ Extracts raw wallet data from the list of URL containing sets of wallets.
        Strips all the unnessecery data and presents it in readable format. """


    for i, set in enumerate(url_list_of_sets):
        print(i)
        precooked_sets_wallet_list = wallet_raw_extractor(set)
        time.sleep(randint(5, 8))
        yield precooked_sets_wallet_list


def wallet_raw_extractor(url_set):
    "Scraps wallets data and returns a list"

    page = requests.get(url_set, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')
    table_1 = soup.find(id="tblOne")  #1-19 wallets
    table_2 = soup.find(id="tblOne2")  #19-100 wallets
    tables = [table_1, table_2]

    new_table = pd.DataFrame(columns=range(0,10), index = [0])
    print(url_set)
    # mixed_wallet_data_table = []
    row_marker = 0
    for table in tables:
        time.sleep(1)
        try:
            for row in table.find_all('tr'):
                wallet = []

                column_marker = 0
                columns = row.find_all('td')

                for column in columns:
                    new_table.iat[row_marker,column_marker] = column.get_text()
                    wallet.append(column.get_text())
                    column_marker += 1

                yield wallet
        except:
            print("Connection lost or IP probably blocked!")
            restart_analyse()
            from sys import exit
            exit(0)
            # break


def register_new_wallet(wallet):
    "Adds new wallets into database"
    wallet[1], wallet[0] = wallet[1], wallet[1]
    wallet[1], wallet[3] = address_filter(wallet[1])
    balance = float(balance_filter(wallet[2]))
    last_in = date_filter(wallet[5])
    last_out = date_filter(wallet[8])
    # print(repr(wallet[9]),wallet[9])
    out_nums = wallet[9] if wallet[9] != '' else '0'
    transactions_delta = int(wallet[6]) - int(out_nums)
    Wallet(wallet_name=wallet[0],
           address=wallet[1],
           balance=balance,
           delta=balance,
           misc=wallet[3],
           last_in=last_in,
           last_out=last_out,
           in_nums=wallet[6],
           out_nums=out_nums,
           transactions_delta=transactions_delta,
           transactions_delta_all=transactions_delta
           ).save()


def update_wallet(db_wallet, wallet, db_wallet_ins, db_wallet_outs):
    "Updates existing wallet"

    old_balance = list(db_wallet.values('balance'))[0].get('balance')
    new_balance = float(balance_filter(wallet[2]))
    # print(new_balance,repr(new_balance))
    delta = float(new_balance) - float(old_balance)

    last_in = date_filter(wallet[5])
    last_out = date_filter(wallet[8])
    # print(wallet)
    in_nums = wallet[6] if wallet[6] != '' else '0'
    out_nums = wallet[9] if wallet[9] != '' else '0'
    tr_delta_old = int(db_wallet_ins) - int(db_wallet_outs)
    tr_delta_new = int(in_nums) - int(out_nums)
    transactions_delta = tr_delta_new - tr_delta_old

    # from django.db import models


    db_wallet.update(balance=new_balance,
                     last_in=last_in,
                     last_out=last_out,
                     in_nums=in_nums,
                     out_nums=out_nums,
                     delta=delta,
                     transactions_delta=transactions_delta,
                     transactions_delta_all=tr_delta_new,
                     updated_at=timezone.now()
                    )


def up_to_date_check(wallet_list):
    """Regiters new wallets to the DB. Updates existing wallets."""
    for wallet in wallet_list:
        if len(wallet) == 0:
            continue

        db_wallet = Wallet.objects.filter(wallet_name=wallet[1])

        if db_wallet.count() == 0:
            register_new_wallet(wallet)
            continue

        wallet_ins = wallet[6]
        wallet_outs = wallet[9]
        db_wallet_ins = list(db_wallet.values('in_nums'))[0].get('in_nums')
        db_wallet_outs = list(db_wallet.values('out_nums'))[0].get('out_nums')

        # if wallet_ins != db_wallet_ins or wallet_outs != db_wallet_outs:
        update_wallet(db_wallet, wallet, db_wallet_ins, db_wallet_outs)



def main(srch_rng, start_pg):
    """ Makes up to date checks for wallets before aggregating.
        Fetches whole list of wallets (max=10000) """
    wallet_sets_url_list = wallet_sets_url_list_maker(srch_rng, start_pg)

    wallets_scraped_data_list = wallet_data_scraper(wallet_sets_url_list)

    "In case of no internet connection"
    try:
        import itertools
        wallets_scraped_data_list = list(itertools.chain.from_iterable(
                                                     wallets_scraped_data_list))
    except:
        exit(1)

    cleaned_wal_scraped_data = [x for x in wallets_scraped_data_list if x != []]
    today_wall_list = Wallet_List.objects.filter(id=1)
    today_wall_list.update(wallet_list=cleaned_wal_scraped_data,
                    updated_at=timezone.now())

    up_to_date_check(wallets_scraped_data_list)
    btc_price = btc_price_extractor()
    print('Wallet search completed. Database updated.')
    return wallets_scraped_data_list, btc_price
