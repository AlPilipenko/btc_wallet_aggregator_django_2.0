import json
from sys import exit
from datetime import datetime, date, time, timedelta
import os
import re
from sys import exit
import time
import shutil
from . import wallet_searcher
from time import time




#with open('my_dict.json', 'w') as f:
    #json.dump(my_dict, f)

# elsewhere...

#with open('my_dict.json') as f:
    #my_dict = json.load(f)
    #print(my_dict.get("ggg"))

def database_transaction_amount_check():
    pass


"Stores wallets and number of transactions"


#file = open(r"C:\Users\PandoraII\Hardway\Aggregator\dict.txt", mode='r')
def data_check(k, v1, v2, my_dict):
    #print(k,v1,v2)

#########################################
    "If first-time entry or new transactions sends to proccessing"
    "Else if info is 'old' gets data from database"
    if my_dict.get(k) == None or my_dict.get(k) != [v1,v2]:
        with open('aggregator/wall_tran.json', 'w') as f:
            #print("HERE!",v1,v2,my_dict.get(k) != v1)
            my_dict[k] = v1,v2
            json.dump(my_dict, f)
            return k
######################################

    elif my_dict.get(k) != None:
        #print("todo")
        return "old_data"

    #print(k, v)
    #exit(0)
    #return w



def wallet_data_record(w):
    "Records wallets data in dictionary and moves old data to folder"
    #with open(r"dataset.json") as d:
        #data_dict = json.load(d)
    # Move a file from the directory d1 to d2
    with open(r'aggregator/datetime_of_last_wallet_data.txt', 'r') as dt:
        r = dt.read()
        r = r.strip()

        new_name = f'{r}.json'

        #shutil.move(r'C:\Users\PandoraII\Hardway\Aggregator\dataset.json', r'C:\Users\PandoraII\Hardway\Aggregator\old_datasets')
        #import shutil
##################################
        "Counting new entries. part1"
        with open(r"aggregator/dataset.json") as ff:
            #print(k,v)
            old_dataset = json.load(ff)
####################################
        shutil.copyfile("aggregator/dataset.json", "aggregator/dataset_copy.json")

        old_file = os.path.join(r'aggregator/', "dataset_copy.json")
        #print(old_file)
        new_file = os.path.join(r'aggregator/old_datasets', new_name)
        os.rename(old_file, new_file)
        #os.rename(r'C:\Users\PandoraII\Hardway\Aggregator\old_datasets\dataset.json', new_name)
        #exit(0)


    t = str(datetime.now())
    t = t[:-7]
    t = re.sub(':', '',t)

    with open(r'aggregator/datetime_of_last_wallet_data.txt', 'w') as dt:
        dt.write(t)

    #time.sleep(5)
    #shutil.move(r'C:\Users\PandoraII\Hardway\Aggregator\dataset.json', r'C:\Users\PandoraII\Hardway\Aggregator\old_datasets')

    with open(r'aggregator/dataset.json') as d:
        #print(k,v)
        data_dict = json.load(d)
        with open(r'aggregator/dataset.json', 'w') as d:
            #data_dict = {}
            #print(data_dict)
            for x in w:
                #print("Before",data_dict)
                #time.sleep(1)
                data_dict[x[4]] = x[:4:], t
                #print("After",data_dict)
            json.dump(data_dict, d)

#######################################
        "Counting new entries. part2"
        with open(r"aggregator/dataset.json") as dd:
            #print(k,v)
            new_dataset = json.load(dd)
        return f"new-wallets entries:{len(new_dataset)-len(old_dataset)}"

#######################################
def wallet_data_extraction(v):
    "Gets data from dataset, also adjust transactions periods accordingly"
    "needed for daily statistics"
    v[2], r = wallet_searcher.filter(v[2])
    #print(v[2], r)
    with open(r"aggregator/dataset.json") as f:
        #print(v)
        my_dict = json.load(f)
        #print(my_dict)
        w = my_dict.get(v[2])
        #print(w)
        try:
            d = w[1]
        except TypeError:
            print("aggregator/dataset/wallet_trans error. Restarting...")
            return None

        #print(d)
        year,month,day = d[:4],d[5:7],d[8:10]
        #print(year,month,day)
        tr_date = date(int(year),int(month),int(day))
        delta = date.today() - tr_date
        str_delta = str(delta)
        #print(str_delta)
        try:
            cut_off = str_delta.index('d')
            days = int(str_delta[:cut_off])
        except ValueError:
            days = 0

        #print(days)


        if days <= 0:
            return [v[0], w[0][1], w[0][2], w[0][3],v[2]]
        elif days <= 6:
            w[0][2][0] = 0
            return [v[0], w[0][1], w[0][2], w[0][3],v[2]]
        elif days <= 29:
            w[0][2][0] = w[0][2][1] = 0
            return [v[0], w[0][1], w[0][2], w[0][3],v[2]]
        elif days <= 89:
            w[0][2][0] = w[0][2][1] = w[0][2][2] = 0
            return [v[0], w[0][1], w[0][2], w[0][3],v[2]]
        elif days <= 179:
            w[0][2][0] = w[0][2][1] = w[0][2][2] = w[0][2][3] = 0
            return [v[0], w[0][1], w[0][2], w[0][3],v[2]]
        elif days <= 364:
            w[0][2][0] = w[0][2][1] = w[0][2][2] = w[0][2][3] = w[0][2][4] = 0
            return [v[0], w[0][1], w[0][2], w[0][3],v[2]]
        elif days > 364:
            w[0][2][0] = w[0][2][1] = w[0][2][2] = w[0][2][3] = w[0][2][4] = w[0][2][5] = 0
            return [v[0], w[0][1], w[0][2], w[0][3],v[2]]

        else:
            print("???, unknown error in data manip")

        #print(w)
        return [v[0], w[0][1], w[0][2], w[0][3],v[2]]
