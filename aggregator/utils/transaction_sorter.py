from sys import exit
from datetime import date, timedelta
from aggregator.models import Wallet


def transaction_raw_extractor(url):
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find(id="table_maina")
    new_table = pd.DataFrame(columns=range(0,5), index = [0])

    row_marker = 0
    try:
        for row in table.find_all('tr'):  # figure out how it works
            my_table = []

            column_marker = 0
            columns = row.find_all('td')

            for i, column in enumerate(columns):
                if i == 1 or i == 2:
                    new_table.iat[row_marker,column_marker] = column.get_text()
                    my_table.append(column.get_text())
                    column_marker += 1
            yield my_table

    except AttributeError:
        # import os
        # os.system("pause")
        print("URL failed:", url)


def period_calc(transactions, address):

    now = date.today()
    last_day = 0
    last_week = 0
    last_month = 0
    last_three_months = 0
    last_six_months = 0
    last_year = 0
    total_sum = 0
    last_two_years = 0
    last_three_years = 0
    last_five_years = 0

    for i, transaction in enumerate(transactions):
        if len(transaction) == 0:
            continue

        amount_cut = str(transaction[1]).find('BTC')
        amount = str(transaction[1][:amount_cut])
        amount = amount.replace(',', '')

        str_trans = str(transaction)
        year, month, day = str_trans[2:6], str_trans[7:9], str_trans[10:12]
        trans_date = date(int(year), int(month), int(day))
        delta = date.today() - trans_date
        str_delta = str(delta)

        try:
            cut = str_delta.index('d')
            days = int(str_delta[:cut])
        except ValueError:
            days = 0

        sign = 'in' if str_trans.find('+') != -1 else 'out'
        if sign == 'in':

            if days <= 0:
                last_day += float(amount)
            elif days <= 6:
                last_week += float(amount)
            elif days <= 29:
                last_month += float(amount)
            elif days <= 89:
                last_three_months += float(amount)
            elif days <= 179:
                last_six_months += float(amount)
            elif days <= 365:
                last_year += float(amount)
            elif days <= 730:
                last_two_years += float(amount)
            elif days <= 1095:
                last_three_years += float(amount)
            elif days <= 1825:
                last_five_years += float(amount)
            total_sum += float(amount)

        else:

            if days <= 0:
                last_day += float(amount)
            elif days <= 6:
                last_week += float(amount)
            elif days <= 29:
                last_month += float(amount)
            elif days <= 89:
                last_three_months += float(amount)
            elif days <= 179:
                last_six_months += float(amount)
            elif days <= 364:
                last_year += float(amount)
            elif days <= 730:
                last_two_years += float(amount)
            elif days <= 1095:
                last_three_years += float(amount)
            elif days <= 1825:
                last_five_years += float(amount)
            total_sum += float(amount)

    last_week += last_day
    last_month += last_week
    last_three_months += last_month
    last_six_months += last_three_months
    last_year += last_six_months
    last_two_years += last_year
    last_three_years += last_two_years
    last_five_years += last_three_years

    db_wallet = Wallet.objects.filter(address=address)
    try:

        db_wallet.update(transactions_delta=[round(last_day),
                                             round(last_week),
                                             round(last_month),
                                             round(last_three_months),
                                             round(last_six_months),
                                             round(last_year),
                                             round(last_two_years),
                                             round(last_three_years),
                                             round(last_five_years),
                                             round(total_sum),
                                             i],

                          up_to_date='yes'   # DONT FORGET TO CHANGE
                        )

    except:
        # import os
        # os.system("pause")
        print("Failed to save transactions:", address)


def values_extractor(url, address):
    "Gets transactions and their time "
    transactions = transaction_raw_extractor(url)

    period_calc(transactions, address)
