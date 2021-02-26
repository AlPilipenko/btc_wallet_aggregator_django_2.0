from django.test import TestCase

# Create your tests here.
from random import randint
import time
from datetime import datetime, date

##############################################################
Starting_Value=1000
Final_Value=150
Percentage_Increase = round(( (Final_Value - Starting_Value) / Starting_Value) *100)
print(Percentage_Increase)
##############################################################

x = {'abc': 'cd'}
word ='b'
print(x.get('a'+word))
















x = '2021-02-24 04:11:00'

# my_bd = date(1988, 1, 6)
print(date.today(), x)
time_delta = date.today() - date(int(x[0:4]) ,int(x[5:7]), int(x[8:10]))
time_delta =str(time_delta)
# time_delta = time_delta[:time_delta.find('d')-1]
# time_delta = int(time_delta)
print(time_delta)

# y = date.now()
#
#
#
# exchanges = ['Huobi',
#              'Poloniex',
#              'Binance',
#              'Kraken',
#              'Huobi',
#              'BitX',
#              'Bittrex',
#              'Bitfinex',
#              'F2Pool',
#              'SlushPool',
#              'BITMEX',
#              'OKEx',
#              'Bitstamp.net'
#             ]
#
#
# misc = '35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP 3-of-7wallet: Huobi-coldwallet'
# for e in exchanges:
#     if misc.find(e) != -1:
#         print('boom')
