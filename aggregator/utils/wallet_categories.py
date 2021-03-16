from aggregator.models import Wallet, Aggregator
from datetime import date

exchanges = ['Huobi',
             'Poloniex',
             'Binance',
             'Kraken',
             'BitX',
             'Bittrex',
             'Bitfinex',
             'F2Pool',
             'SlushPool',
             'BITMEX',
             'OKEx',
             'Bitstamp.net',
             'BetVIP',
             'Xapo',
             'HaoBTC',
            ]

def cat_sorter():
    "Allocates wallets to special category based on wallet performance"
    # Wallet.objects.all().update(category='normal')
    # return ''
    wallets = Wallet.objects.all()

    # wallets = Wallet.objects.all()
    # for wallet in wallets:
    #     balance = float(wallet.__dict__.get('balance'))
    #     print(type(balance))
    #     wallet.__dict__.update(balance=balance)
    #     print(type(wallet.__dict__.get('balance')))

    # wallet.category='marked'


    for wallet in wallets:
        misc = wallet.misc
        in_nums = int(wallet.in_nums)
        out_nums = int(wallet.out_nums)
        total_tr = in_nums + out_nums
        last_in = wallet.last_in
        last_out = wallet.last_out
        time_delta = 0
        category = 'normal'

        # if last_out != '':
        #     # print(last_out)
        #     year, month, day = (int(last_out[0:4]), int(last_out[5:7]),
        #                                                     int(last_out[8:10]))
        #     time_delta = date.today() - date(year, month, day)
        #     time_delta = str(time_delta)
        #     if time_delta == '0:00:00':
        #         continue
        #     else:
        #         time_delta = time_delta[:time_delta.find('d')-1]
        #         time_delta = int(time_delta)

        if misc != '':
            category = 'marked'
            for exchange in exchanges:
                if misc.find(exchange) != -1:
                    category = 'exchange/pool'

        if total_tr > 500 and category != 'exchange/pool':
            category = 'trading'
            if in_nums > 2000 and out_nums > 2000:
                category = 'algo'


        # if category == 'normal' and time_delta > 1825:
        #     category = 'inactive'
        # print("2",category)
        if wallet.category == 'normal' and category == 'normal':
            continue
        else:
            wallet.category = category
            wallet.save()
