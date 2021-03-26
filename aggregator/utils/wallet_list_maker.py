from aggregator.models import Wallet_List, Wallet

def wallet_list_maker_func():
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
        new_wallet_list.append([i+1,
                                wallet.get('address'),
                                round(float(wallet.get('balance'))),
                                wallet.get('in_nums'),
                                wallet.get('out_nums')])
    updated_display_list = Wallet_List.objects.filter(id=1)
    updated_display_list.update(wallet_list_display = new_wallet_list)
