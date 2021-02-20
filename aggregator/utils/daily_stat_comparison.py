import json
class Wallets_Divided_By_Categories():

    def __init__(self, wallets_category, list_of_wallets, yesterday_daily_data):
        self.wallets_category = wallets_category
        self.list_of_wallets = list_of_wallets
        self. yesterday_daily_data = yesterday_daily_data

    def count_transactions_by_period(self):
        all_daily = 0
        all_weekly = 0
        all_monthly = 0
        all_quarterly = 0
        all_half_yearly = 0
        all_yearly = 0
        all_total = 0
        for x in self.list_of_wallets:

            all_daily += x[2][0]
            all_weekly += x[2][1]
            all_monthly += x[2][2]
            all_quarterly += x[2][3]
            all_half_yearly += x[2][4]
            all_yearly += x[2][5]
            all_total += x[2][6]


        return all_daily,all_weekly,all_monthly,all_quarterly,all_half_yearly,all_yearly,all_total



    def transactions_plus_percantage(self):
        all_daily = 0
        all_weekly = 0
        all_monthly = 0
        all_quarterly = 0
        all_half_yearly = 0
        all_yearly = 0
        all_total = 0
        for x in self.list_of_wallets:

            all_daily += x[2][0]
            all_weekly += x[2][1]
            all_monthly += x[2][2]
            all_quarterly += x[2][3]
            all_half_yearly += x[2][4]
            all_yearly += x[2][5]
            all_total += x[2][6]



        #d = f'{round(((x / y[m][n]) * 100) - 100,1)}%'
        #x = f'{x}({d})'
        #f'{0.0}%'
        try:
            all_daily = f'{all_daily}({round(((all_daily / self.yesterday_daily_data[0]) * 100) - 100,1)}%)'
        except ZeroDivisionError:
            all_daily = f'{all_daily}({0.0}%)'

        try:
            all_weekly = f'{all_weekly}({round(((all_weekly / self.yesterday_daily_data[1]) * 100) - 100,1)}%)'
        except ZeroDivisionError:
            all_weekly = f'{all_weekly}({0.0}%)'

        try:
            all_monthly = f'{all_monthly}({round(((all_monthly / self.yesterday_daily_data[2]) * 100) - 100,1)}%)'
        except ZeroDivisionError:
            all_monthly = f'{all_monthly}({0.0}%)'

        try:
            all_quarterly = f'{all_quarterly}({round(((all_quarterly / self.yesterday_daily_data[3]) * 100) - 100,1)}%)'
        except ZeroDivisionError:
            all_quarterly = f'{all_quarterly}({0.0}%)'

        try:
            all_half_yearly = f'{all_half_yearly}({round(((all_half_yearly / self.yesterday_daily_data[4]) * 100) - 100,1)}%)'
        except ZeroDivisionError:
            all_half_yearly = f'{all_half_yearly}{0.0}%)'

        try:
            all_yearly = f'{all_yearly}({round(((all_yearly / self.yesterday_daily_data[5]) * 100) - 100,1)}%)'
        except ZeroDivisionError:
            all_yearly = f'{all_yearly}({0.0}%)'

        try:
            all_total = f'{all_total}({round(((all_total / self.yesterday_daily_data[6]) * 100) - 100,1)}%)'
        except ZeroDivisionError:
            all_total = f'{all_total}({0.0}%)'



        return all_daily,all_weekly,all_monthly,all_quarterly,all_half_yearly,all_yearly,all_total


    def transactions_plus_percantage_backup(self):

        with open (r'daily_stat_data.json','r') as f:
            my_dict = json.load(f)

            for x in my_dict:
                print("!!!!!!!!!!!!!!!!!!!!!",x)

            y = []
            t = []

            yesterday_total = my_dict.get('total')
            yesterday_robots = my_dict.get('robots')
            yesterday_no_token = my_dict.get('no_token')
            yesterday_old = my_dict.get('old')
            yesterday_exchanges = my_dict.get('exchanges')
            yesterday_wallet_token = my_dict.get('wallet_token')

            y.append(yesterday_total)
            y.append(yesterday_robots)
            y.append(yesterday_no_token)
            y.append(yesterday_old)
            y.append(yesterday_exchanges)
            y.append(yesterday_wallet_token)

            t.append(list(total.count_transactions_by_period()))
            t.append(list(robot_tag.count_transactions_by_period()))
            t.append(list(no_token_tag.count_transactions_by_period()))
            t.append(list(old_tag.count_transactions_by_period()))
            t.append(list(exchanges_tag.count_transactions_by_period()))
            t.append(list(wallet_token_tag.count_transactions_by_period()))

            #delta_total = (yesterday_total)
            #print(y_wallet_token)

            #l= [1,2,3,4,6]
            #g = [1.5,4,3,4,50]
            final = []

            n = 0
            m = 0
            for z in t:
                for x in z:
                    try:
                        d = f'{round(((x / y[m][n]) * 100) - 100,1)}%'
                        x = f'{x}({d})'
                        n+=1
                        final.append(x)

                    except ZeroDivisionError:
                        n+=1
                        final.append(f'{0.0}%')
                n = 0
                m += 1

            print(final)

def categorising_wallets(w):
    "break wallet data into categories"
    robots = []
    no_token = []
    old = []
    exchanges = []
    wallet_token = []


    for x in w:
        print(x)
        if x[1] == "None" and x[3] > 500 or x[1] == '>500':
            robots.append(x)

        elif x[1] == "None" or x[1] == 0:
            no_token.append(x)

        elif x[1] == "Old":
            old.append(x)

        elif (x[1].find('Huobi') != -1 or x[1].find('Poloniex') != -1 or x[1].find('Binance') != -1
             or x[1].find('Kraken.com') != -1 or x[1].find('Huobi') != -1 or x[1].find('BitX.co') != -1
             or x[1].find('Bittrex') != -1 or x[1].find('Bitfinex') != -1 or x[1].find('F2Pool') != -1
             or x[1].find('SlushPool.com') != -1):

             exchanges.append(x)

        else:
            wallet_token.append(x)


    with open (r'aggregator/daily_stat_data.json','r') as f:
        my_dict = json.load(f)
        total = Wallets_Divided_By_Categories('total', w, my_dict.get('total'))
        robot_tag = Wallets_Divided_By_Categories('robots',robots, my_dict.get('robots'))
        no_token_tag = Wallets_Divided_By_Categories('no_token',no_token, my_dict.get('no_token'))
        old_tag = Wallets_Divided_By_Categories('old',old, my_dict.get('old'))
        exchanges_tag = Wallets_Divided_By_Categories('exchanges',exchanges, my_dict.get('exchanges'))
        wallet_token_tag = Wallets_Divided_By_Categories('wallet_token',wallet_token, my_dict.get('wallet_token'))
    #print('all_daily',all_daily)
    #print('all_weekly',all_weekly)
    #print('all_monthly',all_monthly)
    #print('all_quarterly',all_quarterly)
    #print('all_half_yearly',all_half_yearly)
    #print('all_yearly',all_yearly)
    #print('all_total',all_total)
    #yesterday_total = my_dict.get('total')
    #yesterday_robots = my_dict.get('robots')
    #yesterday_no_token = my_dict.get('no_token')
    #yesterday_old = my_dict.get('old')
    #yesterday_exchanges = my_dict.get('exchanges')
    #yesterday_wallet_token = my_dict.get('wallet_token')





    with open('aggregator/daily_stat_data.json', 'w') as f:
        daily_stat_data_dict = {
                                'total' : total.count_transactions_by_period(),
                                'robots' : robot_tag.count_transactions_by_period(),
                                'no_token' : no_token_tag.count_transactions_by_period(),
                                'old' : old_tag.count_transactions_by_period(),
                                'exchanges' : exchanges_tag.count_transactions_by_period(),
                                'wallet_token' : wallet_token_tag.count_transactions_by_period()
                                }


        json.dump(daily_stat_data_dict, f)







    print('\n')
    print('\n')
    print('\n')
    print('\t   \tdaily','\t\tweekly','\t\tmonthly','\t\tquarter','\thalf_year','\t\tyear','\t\ttotal' )
    print(len(total.list_of_wallets), total.wallets_category, total.transactions_plus_percantage())
    print(len(robot_tag.list_of_wallets), robot_tag.wallets_category, robot_tag.transactions_plus_percantage())
    print(len(no_token_tag.list_of_wallets), no_token_tag.wallets_category, no_token_tag.transactions_plus_percantage())
    print(len(old_tag.list_of_wallets), old_tag.wallets_category, old_tag.transactions_plus_percantage())
    print(len(exchanges_tag.list_of_wallets), exchanges_tag.wallets_category, exchanges_tag.transactions_plus_percantage())
    print(len(wallet_token_tag.list_of_wallets), wallet_token_tag.wallets_category, wallet_token_tag.transactions_plus_percantage())
