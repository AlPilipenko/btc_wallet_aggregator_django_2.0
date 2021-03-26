import matplotlib
from pylab import rcParams
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from aggregator.models import Aggregator, Category, Wallet, Wallet_List, Plots
from sys import exit

class Main_Plot_Maker():
    # plot_style = 'Solarize_Light2'
    # plot_style = 'fivethirtyeight'
    # plot_style = 'ggplot'
    plot_style = 'dark_background'

    def __init__(self, color, title, name=None):
        self.name = name
        self.color = color
        self.title = title
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
        """Searches DB for the requested column.
           Returns dictionary, where key is column name and
           value is a list of DB values.
        """
        data_container = []
        for k in columns:
            to_search = {}
            to_search[k] = []
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
        return data_container


    def plot_graph_type1(self, columns, xlabel='Balance (BTC)',
                                       save_name=None, title=None, ylabel=None):
        "Plots a graph. Can plot on both 2 and 3 axis"
        plot_data = Main_Plot_Maker.db_plot_data_search(self, columns)
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.rcParams['xtick.labelsize'] = 7


        fig, ax1 = plt.subplots()
        xaxis = list(plot_data[0].values())[0]
        yaxis = list(plot_data[1].values())[0]
        ax1.set_ylabel(xlabel, color = self.color)
        ax1.plot(xaxis, yaxis, color = self.color, linewidth=5,
                                            linestyle='solid',marker='.')
        ax1.set_zorder(1) # for graph to be on top of other graphs
        ax1.tick_params(axis ='y', labelcolor = self.color)
        ax1.tick_params(axis ='x', rotation=45)
        ax1.ticklabel_format(style='plain', axis='y') # to disable sci-notation

        if len(plot_data) > 2:
            yaxis1 = list(plot_data[2].values())[0]
            ax2 = ax1.twinx()
            color = 'tab:green'
            ax2.set_ylabel('% change', color=color)
            ax2.plot(xaxis, yaxis1, color=color)
            ax2.set_zorder(2)
            ax2.patch.set_visible(False)
            ax2.tick_params(axis ='y', labelcolor = color)
            plt.title(self.title, fontweight ="bold", fontsize=12)
            ax2.grid(False)

        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(4.4, 4.4)

        # if Main_Plot_Maker.plot_style == 'Solarize_Light2':
        #     if save_name != None:
        #         ax2.set_ylabel(ylabel, color=color)
        #         plt.title(title, fontweight ="bold",fontsize=12)
        #         plt.savefig('aggregator/static/plots/' + save_name +'_plot.png',
        #                                                     bbox_inches='tight')
        #     else:
        #         plt.savefig('aggregator/static/plots/' + save_name +'_plot.png',
        #                                                     bbox_inches='tight')
        # else:
        #     plt.grid(False)
        #     if save_name != None:
        #         ax2.set_ylabel(ylabel, color=color)
        #         plt.title(title, fontweight ="bold",fontsize=12)
        #         plt.savefig('aggregator/static/plots/'+save_name+'_plot_dark.png',
        #                                                     bbox_inches='tight')
        #     else:
        #         plt.savefig('aggregator/static/plots/'+self.name+'_plot_dark.png',
        #                                                     bbox_inches='tight')


        url = 'media/aggregator/plots/'
        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            if save_name != None:
                ax2.set_ylabel(ylabel, color=color)
                plt.title(title, fontweight ="bold",fontsize=12)
                name = save_name +'_plot.png'
            else:
                name = self.name +'_plot.png'
        else:
            plt.grid(False)
            if save_name != None:
                ax2.set_ylabel(ylabel, color=color)
                plt.title(title, fontweight ="bold",fontsize=12)
                name = save_name +'_plot_dark.png'
            else:
                name = self.name + '_plot_dark.png'


        # plot_path = url + name
        # plt.savefig(plot_path, bbox_inches='tight')
        # plot_instance = Plots()
        # plot_instance.plot_name = name
        # plot_instance.plot = plot_path[6:]
        # plot_instance.save()

        plot_path = url + name
        plt.savefig(plot_path, bbox_inches='tight')
        db_plot = Plots.objects.filter(plot_name=name)
        db_plot.update(plot=plot_path[6:])

        plt.close('Figure')
        plt.close('all')


    def plot_graph_type2(self, *args):
        "Plots graph of aggregations of different categories"
        plt.style.use(Main_Plot_Maker.plot_style)
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        # plt.rcParams['xtick.labelsize'] = 7
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

        db_aggregator = Aggregator.objects.all()
        db_category = Category.objects.all()

        for agg in db_aggregator:
            date = agg.__dict__.get('aggregation_date')
            # print(date)
            # date = list(date.values())[0]
            date = str(date)[:10]
            dates.append(date)
            balance = agg.__dict__.get('balance')
            all_balance.append(float(balance))
            btc_price = agg.__dict__.get('btc_price')
            btc_price_list.append(int(btc_price))
            # delta = agg.__dict__.get('delta')
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

        fig, ax = plt.subplots()

        fig = matplotlib.pyplot.gcf()
        fig.set_size_inches(5,5)
        ax.set_ylabel('Balance (BTC)', color = self.color)
        plt.plot(dates,marked_balance, color='r', linewidth=2,linestyle='solid',
                                        label='interesting wallets aggregation')
        plt.plot(exchanges_balance, color='y', linewidth=2, linestyle='solid',
                                                  label='exchanges aggregation')
        plt.plot(algo_balance, color='m', linewidth=2, linestyle='solid',
                                                label='high volume aggregation')
        plt.plot(trading_balance, color='c', linewidth=2, linestyle='solid',
                                              label='medium volume aggregation')
        plt.plot(btc_price_list, color='g', linewidth=2, linestyle='solid',
                                                              label='BTC price')
        ax.set_zorder(1) # for graph to be on top of other graphs
        ax.tick_params(axis ='y', labelcolor = self.color)
        ax.tick_params(axis ='x', rotation=45)
        ax.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax.ticklabel_format(style='plain', axis='y')
        plt.xticks(rotation=45,fontsize=7)
        plt.legend(fontsize=7) # to display graphs labels
        plt.ticklabel_format(style='plain', axis='y') # to disable sci-notation
        plt.yscale("log")
        plt.title('All aggregations and all categories',
                                                 fontweight ="bold",fontsize=12)

        # if Main_Plot_Maker.plot_style == 'Solarize_Light2':
        #     plt.savefig('aggregator/static/plots/' + 'combined' + '_plot.png',
        #                                                     bbox_inches='tight')
        # else:
        #     plt.savefig('aggregator/static/plots/'+'combined'+'_plot_dark.png',
        #                                                     bbox_inches='tight')

        url = 'media/aggregator/plots/'
        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            name = 'combined_plot.png'
        else:
            name = 'combined_plot_dark.png'
        # plot_path = url + name
        # plt.savefig(plot_path, bbox_inches='tight')
        # plot_instance = Plots()
        # plot_instance.plot_name = name
        # plot_instance.plot = plot_path[6:]
        # plot_instance.save()

        plot_path = url + name
        plt.savefig(plot_path, bbox_inches='tight')
        db_plot = Plots.objects.filter(plot_name=name)
        db_plot.update(plot=plot_path[6:])

        plt.close('all')


    def plot_scatter_type1():
        "plots scatterplot of balances vs transactions"
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

        rcParams['figure.figsize'] = 5.2, 5.2
        plt.scatter(num_of_tr, balances, c=ratio, cmap='summer',
                               edgecolor='black', linewidth=1, alpha=0.75, s=30)
        cbar = plt.colorbar()
        cbar.set_label('Ratio (Balance / All transactions)')
        plt.yscale("log")
        plt.xscale("log")
        plt.title('Wallets balances and transactions',fontsize=12,
                                                        fontweight ="bold")
        plt.ylabel('Balance (BTC)')
        plt.xlabel('Sum of all wallets transactions')
        # if Main_Plot_Maker.plot_style == 'Solarize_Light2':
        #     plt.savefig('aggregator/static/plots/bal_tr_scatter.png',
        #                                                     bbox_inches='tight')
        # else:
        #     plt.savefig('aggregator/static/plots/bal_tr_scatter_dark.png',
        #                                                     bbox_inches='tight')

        url = 'media/aggregator/plots/'
        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            name = 'bal_tr_scatter.png'
        else:
            name = 'bal_tr_scatter_dark.png'
        # plot_path = url + name
        # plt.savefig(plot_path, bbox_inches='tight')
        # plot_instance = Plots()
        # plot_instance.plot_name = name
        # plot_instance.plot = plot_path[6:]
        # plot_instance.save()

        plot_path = url + name
        plt.savefig(plot_path, bbox_inches='tight')
        db_plot = Plots.objects.filter(plot_name=name)
        db_plot.update(plot=plot_path[6:])

        plt.close('all')


    def plot_scatter_type2():
        "Plots scatterplot of balances vs transactions by categories"
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
            balances.append(float(balance))
            num_of_tr.append(float(tr_sum))

            if category == 'normal':
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

        categories =  {
                        'grey' :'normal' ,
                        'red' :'interesting' ,
                        'yellow' :'exchange/pool',
                        'magenta' :'high volume' ,
                        'cyan' :'medium volume',
                      }

        rcParams['figure.figsize'] = 5.2, 5.2
        for tr, bal, color in zip(num_of_tr, balances, colors):
            cat = categories.get(color)
            if cat != None:
                plt.scatter(tr, bal, c=color, s=30, edgecolor='black',
                                                         linewidth=1, label=cat)
                categories.pop(color)
            else:
                plt.scatter(tr, bal, c=color, s=30, edgecolor='black',
                                                                    linewidth=1)
        # rcParams['figure.figsize'] = 4.4, 4.4
        plt.legend()
        plt.yscale("log")
        plt.xscale("log")
        plt.title('Balances and transactions by categories',fontsize=12,
                                                            fontweight ="bold")
        plt.ylabel('Balance (BTC)')
        plt.xlabel('Sum of all wallets transactions')

        # if Main_Plot_Maker.plot_style == 'Solarize_Light2':
        #     plt.savefig('aggregator/static/plots/bal_tr_cat_scatter.png',
        #                                                     bbox_inches='tight')
        # else:
        #     plt.savefig('aggregator/static/plots/bal_tr_cat_scatter_dark.png',
        #                                                     bbox_inches='tight')

        url = 'media/aggregator/plots/'
        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            name = 'bal_tr_cat_scatter.png'
        else:
            name = 'bal_tr_cat_scatter_dark.png'
        # plot_path = url + name
        # plt.savefig(plot_path, bbox_inches='tight')
        # plot_instance = Plots()
        # plot_instance.plot_name = name
        # plot_instance.plot = plot_path[6:]
        # plot_instance.save()

        plot_path = url + name
        plt.savefig(plot_path, bbox_inches='tight')
        db_plot = Plots.objects.filter(plot_name=name)
        db_plot.update(plot=plot_path[6:])

        plt.close('all')


    def plot_pie_type1():
        "Makes pie chart"
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)
        categories = ['normal', 'exchange/pool', 'marked',  'algo', 'trading']
        colors = ['grey', 'yellow', 'red','magenta', 'cyan']
        slices = []
        labels = []
        wallet_today_list = str(Wallet_List.objects.filter(id=1)[0].wallet_list)

        for c in categories:
            db_wallets = Wallet.objects.filter(category=c)
            slice = len(db_wallets)
            for wallet in db_wallets:
                wallet_name = wallet.wallet_name
                if wallet_today_list.find(wallet_name) == -1:
                    slice -= 1
                    continue
            c = 'interesting' if c == 'marked' else c
            c = 'high volume' if c == 'algo' else c
            c = 'medium volume' if c == 'trading' else c
            label = c + ' - ' + str(slice)
            labels.append(label)
            slices.append(slice)

        rcParams['figure.figsize'] = 4.6, 4.6
        textprops = {"fontsize":8}
        plt.pie(slices, colors=colors, labels=labels,
                            wedgeprops={'edgecolor': 'black'},
                            shadow=True, textprops=textprops)

        plt.title("Wallets in each category", fontweight ="bold", fontsize=10)
        plt.tight_layout()

        # if Main_Plot_Maker.plot_style == 'Solarize_Light2':
        #     plt.savefig('aggregator/static/plots/wall_cat_pie.png')
        # else:
        #     plt.savefig('aggregator/static/plots/wall_cat_pie_dark.png')

        url = 'media/aggregator/plots/'
        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            name = 'wall_cat_pie.png'
        else:
            name = 'wall_cat_pie_dark.png'
        # plot_path = url + name
        # plt.savefig(plot_path)
        # plot_instance = Plots()
        # plot_instance.plot_name = name
        # plot_instance.plot = plot_path[6:]
        # plot_instance.save()

        plot_path = url + name
        plt.savefig(plot_path)
        db_plot = Plots.objects.filter(plot_name=name)
        db_plot.update(plot=plot_path[6:])

        plt.close('all')


    def plot_pie_type2():
        "Makes pie chart"
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)
        categories = ['normal', 'exchange/pool', 'marked', 'algo', 'trading']
        colors = ['grey', 'yellow', 'red','magenta', 'cyan']
        slices = []
        labels = []
        wallet_today_list = str(Wallet_List.objects.filter(id=1)[0].wallet_list)

        for c in categories:
            cat_sum = 0
            slice = Wallet.objects.filter(category=c)

            for s in slice:
                wallet_name = s.wallet_name
                if wallet_today_list.find(wallet_name) == -1:
                    continue
                in_nums = s.__dict__.get('in_nums')
                out_nums = s.__dict__.get('out_nums')
                tr_sum = float(in_nums) + float(out_nums)
                cat_sum += tr_sum
            c = 'interesting' if c == 'marked' else c
            c = 'high volume' if c == 'algo' else c
            c = 'medium volume' if c == 'trading' else c
            label = c + ' - ' + str(round(cat_sum))
            labels.append(label)
            slices.append(cat_sum)

        rcParams['figure.figsize'] = 4.6, 4.6
        textprops = {"fontsize":8}
        plt.pie(slices, colors=colors, labels=labels,
                            wedgeprops={'edgecolor': 'black'},
                            shadow=True, textprops=textprops)
        plt.title("All wallets transactions in each category",
                                                fontweight ="bold", fontsize=10)
        plt.tight_layout()

        # if Main_Plot_Maker.plot_style == 'Solarize_Light2':
        #     plt.savefig('aggregator/static/plots/wall_tr_cat_pie.png')
        # else:
        #     plt.savefig('aggregator/static/plots/wall_tr_cat_pie_dark.png')

        url = 'media/aggregator/plots/'
        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            name = 'wall_tr_cat_pie.png'
        else:
            name = 'wall_tr_cat_pie_dark.png'
        # plot_path = url + name
        # plt.savefig(plot_path)
        # plot_instance = Plots()
        # plot_instance.plot_name = name
        # plot_instance.plot = plot_path[6:]
        # plot_instance.save()

        plot_path = url + name
        plt.savefig(plot_path)
        db_plot = Plots.objects.filter(plot_name=name)
        db_plot.update(plot=plot_path[6:])

        plt.close('all')


    def plot_pie_type3():
        "Makes pie chart"
        plt.style.use(['default', 'seaborn-paper'])
        plt.style.use(Main_Plot_Maker.plot_style)
        categories = ['normal', 'marked', 'exchange/pool', 'algo', 'trading']
        colors = ['grey', 'red', 'yellow','magenta', 'cyan']
        slices = []
        labels = []
        wallet_today_list = str(Wallet_List.objects.filter(id=1)[0].wallet_list)

        for c in categories:
            cat_sum = 0
            slice = Wallet.objects.filter(category=c)
            for s in slice:
                wallet_name = s.wallet_name
                if wallet_today_list.find(wallet_name) == -1:
                    continue
                balance = s.__dict__.get('balance')
                cat_sum += float(balance)
            c = 'interesting' if c == 'marked' else c
            c = 'high volume' if c == 'algo' else c
            c = 'medium volume' if c == 'trading' else c
            label = c + ' - ' + str(round(cat_sum))
            labels.append(label)
            slices.append(cat_sum)

        rcParams['figure.figsize'] = 4.6, 4.6
        textprops = {"fontsize":8}
        plt.pie(slices, colors=colors, labels=labels,
             wedgeprops={'edgecolor': 'black'},shadow=True, textprops=textprops)
        plt.title("Recorded wallets balance in each category",
                                                fontweight ="bold", fontsize=10)
        plt.tight_layout()



        url = 'media/aggregator/plots/'
        if Main_Plot_Maker.plot_style == 'Solarize_Light2':
            name = 'wall_bal_cat_pie.png'
        else:
            name = 'wall_bal_cat_pie_dark.png'
        # plot_path = url + name
        # plt.savefig(plot_path)
        # plot_instance = Plots()
        # plot_instance.plot_name = name
        # plot_instance.plot = plot_path[6:]
        # # print(plot_path[6:])
        # plot_instance.save()

        plot_path = url + name
        plt.savefig(plot_path)
        db_plot = Plots.objects.filter(plot_name=name)
        db_plot.update(plot=plot_path[6:])

        plt.close('all')
