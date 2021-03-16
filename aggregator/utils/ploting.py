import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from aggregator.models import Aggregator, Category, Wallet
from sys import exit

class Main_Plot_Maker():
    # plot_style = 'Solarize_Light2'  #fivethirtyeight ggplot dark_background Solarize_Light2
    # plot_style = 'Solarize_Light2'
    plot_style = 'dark_background'

    def __init__(self, color, title, name=None):
        self.name = name
        self.color = color
        self.title = title
        # self.delta_per = delta_per


        self.xlabel = 'Aggregation date'
        self.ylabel = 'Balance (BTC)'

        if name == 'all':
            self.db = Aggregator.objects.all()
        else:
            self.db = Category.objects.all()


    "Adding decorator to turn regular method to class method"
    @classmethod # to recieve a class as our first argument in method
    def change_style(cls, style):
        cls.plot_style = style


    def db_plot_data_search(self, columns):
        "Description"
        # print(columns)
        data_container = []
        for a in columns:
            to_search = {}
            to_search[a] = []
            data_container.append(to_search)

        for agg in self.db:
            for to_search in data_container:
                k = list(to_search.keys())[0]
                temp_data = agg.__dict__.get(k)
                temp_value = to_search.get(k)
                try:
                    temp_data = float(temp_data)
                except:
                    pass
                temp_value.append(temp_data)
                to_search[k] = temp_value
            # print(len(temp_value))
        return data_container


    def plot_type1(self, columns, xlabel='Balance (BTC)', save_name=None, title=None, ylabel=None):
        "Description"
        plot_data = Main_Plot_Maker.db_plot_data_search(self, columns)
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.rcParams['xtick.labelsize']=7
        # plt.figure(figsize=(12,10))

        fig, ax1 = plt.subplots()
        # fig.set_size_inches(8, 10)
        xaxis = list(plot_data[0].values())[0]
        yaxis = list(plot_data[1].values())[0]
        ax1.set_ylabel(xlabel, color = self.color)
        ax1.plot(xaxis, yaxis, color = self.color, linewidth=5,
                                            linestyle='solid',marker='.')
        ax1.set_zorder(1) # for graph to be on top of other graphs
        # ax1.patch.set_visible(False)
        ax1.tick_params(axis ='y', labelcolor = self.color)
        ax1.tick_params(axis ='x', rotation=45)
        # ax1.xaxis.set_tick_params(fontsize=7)
        ax1.ticklabel_format(style='plain', axis='y') # to disable sci-notation
        # ax1.set_yscale('log')
        if len(plot_data) > 2:

            yaxis1 = list(plot_data[2].values())[0]
            ax2 = ax1.twinx()
            color = 'tab:green'
            ax2.set_ylabel('% change', color=color)
            ax2.plot(xaxis, yaxis1, color=color)
            ax2.set_zorder(2)
            ax2.patch.set_visible(False)
            ax2.tick_params(axis ='y', labelcolor = color)
            plt.title(self.title, fontweight ="bold")    # Adding title
            ax2.grid(False)


        # print(Main_Plot_Maker.plot_style)
        if Main_Plot_Maker.plot_style == 'Solarize_Light2':

            if save_name != None:

                ax2.set_ylabel(ylabel, color=color)
                plt.title(title, fontweight ="bold")
                plt.savefig('aggregator/static/' + save_name + '_plot.png', bbox_inches='tight')
            else:
                plt.savefig('aggregator/static/' + self.name + '_plot.png', bbox_inches='tight')
        else:
            plt.grid(False)
            if save_name != None:

                ax2.set_ylabel(ylabel, color=color)
                plt.title(title, fontweight ="bold")
                plt.savefig('aggregator/static/' + save_name + '_plot_dark.png', bbox_inches='tight')
            else:
                plt.savefig('aggregator/static/' + self.name + '_plot_dark.png', bbox_inches='tight')
        plt.close('Figure')
        plt.close('all')


    def plot_type2(self, *args):
        "Description"
        plt.style.use(Main_Plot_Maker.plot_style)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)

        # plt.figure(figsize=(15,20))
        # print("plot_type2 - plot style", Main_Plot_Maker.plot_style)


        # plt.xlabel('Aggregation date')
        # plt.ylabel('Balance (BTC)')
        # plt.title('The most rich BTC wallets aggregation')

        # fig = plt.figure()
        # ax = fig.add_subplot(111)


        # plot_data = Main_Plot_Maker.db_plot_data_search(self, *args)
        dates = []
        all_balance = []
        marked_balance = []
        exchanges_balance = []
        algo_balance = []
        trading_balance = []
        all_balance_per = []
        marked_balance_per = []
        exchanges_balance_per = []
        algo_balance_per = []
        trading_balance_per = []
        btc_price_list = []
        # z = []
        db_aggregator = Aggregator.objects.all()
        db_category = Category.objects.all()
        for agg in db_aggregator:
            date = agg.__dict__.get('aggregation_date')
            date = str(date)[:10]
            balance = agg.__dict__.get('balance')
            delta = agg.__dict__.get('delta')
            dates.append(date)
            all_balance.append(float(balance))

            btc_price = agg.__dict__.get('btc_price')
            btc_price_list.append(int(btc_price))
            # z.append(float(delta))

        for agg in db_category:
            balance = agg.__dict__.get('marked_balance')
            marked_balance.append(float(balance))

            balance = agg.__dict__.get('exchanges_balance')
            exchanges_balance.append(float(balance))

            balance = agg.__dict__.get('algo_balance')
            algo_balance.append(float(balance))

            balance = agg.__dict__.get('trading_balance')
            trading_balance.append(float(balance))
        # print(dates)

        fig, ax = plt.subplots()
        # fig.set_size_inches(15,20)
        # fig = plt.gcf()
        # plt.grid(True)
        ax.set_ylabel('Balance (BTC)', color = self.color)
        # ax.plot(dates, all_balance, color='b', linewidth=3, linestyle='solid',marker='o', label='All aggregation')
        plt.plot(dates,marked_balance, color='r', linewidth=1, linestyle='solid',marker='.', label='Interesting wallets aggregation')
        plt.plot(exchanges_balance, color='y', linewidth=1, linestyle='solid',marker='.', label='Exchanges aggregation')
        plt.plot(algo_balance, color='m', linewidth=1, linestyle='solid',marker='.', label='High volume aggregation')
        plt.plot(trading_balance, color='c', linewidth=1, linestyle='solid',marker='.', label='Medium voolume aggregation')
        plt.plot(btc_price_list, color='g', linewidth=1, linestyle='solid',marker='.', label='BTC price')
        ax.set_zorder(1) # for graph to be on top of other graphs
        # ax.patch.set_visible(False)
        ax.tick_params(axis ='y', labelcolor = self.color)
        ax.tick_params(axis ='x', rotation=45)
        # ax.xaxis.set_tick_params(fontsize=7)
        ax.ticklabel_format(style='plain', axis='y')
        # plot = plt.plot(x, z,label='Delta')
        plt.xticks(rotation=45,fontsize=7)
        plt.legend(fontsize=7) # to display graphs labels
        plt.ticklabel_format(style='plain', axis='y') # to disable sci-notation
        plt.yscale("log")
        plt.title('All aggregations and all categories', fontweight ="bold")

        if Main_Plot_Maker.plot_style == 'Solarize_Light2':

            plt.savefig('aggregator/static/' + 'combined' + '_plot.png', bbox_inches='tight')
        else:
            plt.savefig('aggregator/static/' + 'combined' + '_plot_dark.png', bbox_inches='tight')

        plt.close('all')




    def plot_type3():
        plt.style.use(Main_Plot_Maker.plot_style)
        balances = []
        num_of_tr = []
        ratio = []
        db_wallets = Wallet.objects.all()

        for w in db_wallets[:10001]:
            balance = w.__dict__.get('balance')
            in_nums = w.__dict__.get('in_nums')
            out_nums = w.__dict__.get('out_nums')

            tr_sum = float(in_nums) + float(out_nums)
            rat = round(float(balance) / float(tr_sum))
            balances.append(float(balance))
            num_of_tr.append(float(tr_sum))
            ratio.append(rat)

        plt.scatter(num_of_tr, balances, c=ratio, cmap='summer',
                                    edgecolor='black', linewidth=1, alpha=0.75)
        cbar = plt.colorbar()
        cbar.set_label('Ratio (Balance / All transactions)')
        plt.yscale("log")
        plt.xscale("log")
        plt.title('Scatterplot of wallet ballances and transactions',
                                                        fontweight ="bold")
        plt.ylabel('Balance (BTC)')
        plt.xlabel('Sum of all wallet transactions')

        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            plt.savefig('aggregator/static/bal_tr_scatter.png', bbox_inches='tight')
        else:
            plt.savefig('aggregator/static/bal_tr_scatter_dark.png', bbox_inches='tight')

        plt.close('all')

    def plot_type4():
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)

        balances = []
        num_of_tr = []
        colors = []

        db_wallets = Wallet.objects.all()

        for w in db_wallets[:10001]:
            balance = w.__dict__.get('balance')
            category = w.__dict__.get('category')
            in_nums = w.__dict__.get('in_nums')
            out_nums = w.__dict__.get('out_nums')

            tr_sum = float(in_nums) + float(out_nums)
            # rat = round(float(balance) / float(tr_sum))
            balances.append(float(balance))
            num_of_tr.append(float(tr_sum))
            # cat.append(category)
            # num_of_tr.append(float(tr_sum))
            # print(category)
            if category == 'normal':
                if tr_sum > 10**4:
                    print(w)

                color = 'grey'
            elif category == 'marked':
                color = 'red'
            elif category == 'exchange/pool':
                color = 'yellow'
            elif category == 'algo':
                color = 'magenta'
            elif category == 'trading':
                color = 'cyan'


            colors.append(color)
            # ratio.append(rat)

        # import itertools
        # colors = itertools.cycle(["r", "b", "g"])

        for b, tr, c in zip(num_of_tr, balances, colors):
            plt.scatter(b, tr, color=c, label=c)
            #plt.scatter(b, tr, color=c, label=c, s=20)
        # import matplotlib.cm as cm
        #
        #
        #
        # colors = cm.rainbow(np.linspace(0, 1, len(ys)))
        # for y, c in zip(ys, colors):
        #     plt.scatter(x, y, color=c)

        # plt.scatter(balances, num_of_tr, c=ratio, cmap='summer',
        #                             edgecolor='black', linewidth=1, alpha=0.75)
        # cbar = plt.colorbar()
        # cbar.set_label('Ratio')
        plt.yscale("log")
        plt.xscale("log")
        plt.title('Scatterplot of wallet ballances and transactions by categories',
                                                            fontweight ="bold")
        plt.ylabel('Balance (BTC)')
        plt.xlabel('Sum of all wallet transactions')

        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            plt.savefig('aggregator/static/bal_tr_cat_scatter.png', bbox_inches='tight')
        else:
            plt.savefig('aggregator/static/bal_tr_cat_scatter_dark.png', bbox_inches='tight')


        plt.close('all')


    def plot_type5():
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)
        categories = ['normal', 'marked', 'exchange/pool', 'algo', 'trading']
        colors = ['grey', 'red', 'yellow','magenta', 'cyan']
        slices = []
        labels = []

        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()



        for c in categories:
            slice = len(Wallet.objects.filter(category=c))
            label = c + ' - ' + str(slice)
            labels.append(label)
            slices.append(slice)



        plt.pie(slices, colors=colors, labels=labels, wedgeprops={'edgecolor': 'black'}, shadow=True)
        plt.title("Wallets in each category", fontweight ="bold")
        plt.tight_layout()

        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            plt.savefig('aggregator/static/wall_cat_pie.png', bbox_inches='tight')
        else:
            plt.savefig('aggregator/static/wall_cat_pie_dark.png', bbox_inches='tight')

        plt.close('all')



    def plot_type6():
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)
        categories = ['normal', 'exchange/pool', 'marked', 'algo', 'trading']
        colors = ['grey', 'yellow', 'red','magenta', 'cyan']
        slices = []
        labels = []

        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()



        for c in categories:
            cat_sum = 0
            slice = Wallet.objects.filter(category=c)
            for s in slice:
                in_nums = s.__dict__.get('in_nums')
                out_nums = s.__dict__.get('out_nums')

                tr_sum = float(in_nums) + float(out_nums)

                cat_sum += tr_sum
            label = c + ' - ' + str(round(cat_sum))
            labels.append(label)
            slices.append(cat_sum)



        plt.pie(slices, colors=colors, labels=labels, wedgeprops={'edgecolor': 'black'}, shadow=True)
        plt.title("Wallets transactions in each category", fontweight ="bold")
        plt.tight_layout()

        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            plt.savefig('aggregator/static/wall_tr_cat_pie.png', bbox_inches='tight')
        else:
            plt.savefig('aggregator/static/wall_tr_cat_pie_dark.png', bbox_inches='tight')

        plt.close('all')


    def plot_type7():
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)
        categories = ['normal', 'marked', 'exchange/pool', 'algo', 'trading']
        colors = ['grey', 'red', 'yellow','magenta', 'cyan']
        slices = []
        labels = []

        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()
        # normal_wallets = Wallet.objects.all()



        for c in categories:
            cat_sum = 0
            slice = Wallet.objects.filter(category=c)
            for s in slice:
                balance = s.__dict__.get('balance')
                # out_nums = s.__dict__.get('out_nums')

                # tr_sum = float(in_nums) + float(out_nums)

                cat_sum += float(balance)
            label = c + ' - ' + str(round(cat_sum))
            labels.append(label)
            slices.append(cat_sum)



        plt.pie(slices, colors=colors, labels=labels, wedgeprops={'edgecolor': 'black'}, shadow=True)
        plt.title("Wallets balance in each category", fontweight ="bold")
        plt.tight_layout()

        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            plt.savefig('aggregator/static/wall_bal_cat_pie.png', bbox_inches='tight')
        else:
            plt.savefig('aggregator/static/wall_bal_cat_pie_dark.png', bbox_inches='tight')

        plt.close('all')
