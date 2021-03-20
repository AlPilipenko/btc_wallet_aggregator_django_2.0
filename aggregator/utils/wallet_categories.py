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
    
    for wallet in wallets:
        misc = wallet.misc
        in_nums = int(wallet.in_nums)
        out_nums = int(wallet.out_nums)
        total_tr = in_nums + out_nums
        last_in = wallet.last_in
        last_out = wallet.last_out
        time_delta = 0
        category = 'normal'

        if misc != '':
            category = 'marked'
            for exchange in exchanges:
                if misc.find(exchange) != -1:
                    category = 'exchange/pool'

        if total_tr > 500 and category != 'exchange/pool':
            category = 'trading'
            if in_nums > 2000 and out_nums > 2000:
                category = 'algo'

        if wallet.category == 'normal' and category == 'normal':
            continue
        else:
            wallet.category = category
            wallet.save()
