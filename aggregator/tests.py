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


def sorter():
    "Allocates wallets to special category based on wallet performance"
    # Wallet.objects.all().update(category='normal')
    # return ""
    wallets = Wallet.objects.filter(category='normal').all()

    # wallets = Wallet.objects.all()
    # for wallet in wallets:
    #     balance = float(wallet.__dict__.get('balance'))
    #     print(type(balance))
    #     wallet.__dict__.update(balance=balance)
    #     print(type(wallet.__dict__.get('balance')))


    for wallet in wallets[:1000]:
        misc = wallet.__dict__.get('misc')

        # in_nums = int(wallet.__dict__.get('in_nums'))
        # out_nums = int(wallet.__dict__.get('out_nums'))
        # total_tr = in_nums + out_nums
        #
        # last_in = wallet.__dict__.get('last_in')
        # last_out = wallet.__dict__.get('last_out')
        # time_delta = 0
        #
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
            if wallet.wallet_name == '1NDyJtNTjmwk5xPNhjgAMu4HDHigtobu1swallet: Binance-wallet':
                print(wallet)
            wallet.category='marked'
            wallet.save()

        if misc != '':
            if wallet.wallet_name == '1BCEtYsVj9vYEBCWMCNVAPEJoPwVuQwitwallet: 54750128':
                print(wallet)
            # wallet.category='marked'
            # wallet.save()
            # for exchange in exchanges:
            #     if misc.find(exchange) != -1:
            #         wallet.__dict__.update(category='exchange/pool')
                    # wallet.save()
        # if total_tr > 500 and wallet.__dict__.get('category') != 'exchange/pool':
        #     wallet.__dict__.update(category='trading')
        #     if in_nums > 2000 and out_nums > 2000:
        #         wallet.__dict__.update(category='algo')
        #
        # if wallet.__dict__.get('category') == 'normal' and time_delta > 1825:
        #     wallet.__dict__.update(category='inactive')

        # wallet.save()
