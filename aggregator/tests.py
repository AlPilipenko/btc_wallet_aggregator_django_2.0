from django.test import TestCase

# Create your tests here.

import time
print("start")
time.sleep(5)
print("star2t")



# x = [
# 0.0001 ,
# -3500.000381 ,
# -4500.002983 ,
# 2000 ,
# 4000 ,
# 5000 ,
# 6000 ,
# 5000 ,
# 11000 ,
# 5000 ,
# -4500.00033 ,
# -2500.000345 ,
# -6000.000403 ,
# -4500.001477 ,
# 15500 ,
# 6000 ,
# 2000 ,
# 15010 ,
# -3000.000275 ,
# -3500.0022491 ,
# 0.00003333 ,
# 0.00000777 ,
# 8000 ,
# -4500.00138141 ,
# 0.00000547 ,
# 0.00000371 ,
# 0.0001 ,
# 0.0001097 ,
# -8500.00062244 ,
# -6500.00058391 ,
# -10000.00034496 ,
# -5000.00020292 ,
# -7500.00025764 ,
# -2500.00025741 ,
# -7500.00022344 ,
# -6000.00032992 ,
# -12000.00006886 ,
# -5000.00006224 ,
# -16000.00003352 ,
# -15000.00010019 ,
# 0.00001 ,
# -15000.00008735 ,
# 0.00011314 ,
# -6000.00013841 ,
# 0.00000777 ,
# 47000 ,
# -500.00023517 ,
# 20000 ,
# 5000 ,
# 25000 ,
# 50000 ,
# 36001 ,
# -0.1334 ,
# 0.1234 ,
# 0.01 ,
# ]
# a = 0
# for n in x:
#     a += n
# print(sum(x))
#
#
# y = [
#  0.0001,
# -3500.000381,
# -4500.002983,
# 2000,
# 4000,
# 5000,
# 6000,
# 5000,
# 11000,
# 5000,
# -4500.00033,
# -2500.000345,
# -6000.000403,
# -4500.001477,
# 15500,
# 6000,
# 2000,
# 15010,
# -3000.000275,
# -3500.0022491,
# 0.00003333,
# 0.00000777,
# 8000,
# -4500.00138141,
# 0.00000547,
# 0.00000371,
# 0.0001,
# 0.0001097,
# -8500.00062244,
# -6500.00058391,
# -10000.00034496,
# -5000.00020292,
# -7500.00025764,
# -2500.00025741,
# -7500.00022344,
# -6000.00032992,
# -12000.00006886,
# -5000.00006224,
# -16000.00003352,
# -15000.00010019,
# 0.00001,
# -15000.00008735,
# 0.00011314,
# -6000.00013841,
# 0.00000777,
# 47000,
# -500.00023517,
# 20000,
# 5000,
# 25000,
# 50000,
# 36001,
# -0.1334,
# 0.1234,
# 0.01,
# ]
#
# z = [+0.0001,
# -3500.000381,
# -4500.002983,
# +2000,
# +4000,
# +5000,
# +6000,
# +5000,
# +11000,
# +5000,
# -4500.00033,
# -2500.000345,
# -6000.000403,
# -4500.001477,
# +15500,
# +6000,
# +2000,
# +15010,
# -3000.000275,
# -3500.0022491,
# +0.00003333,
# +0.00000777,
# +8000,
# -4500.00138141,
# +0.00000547,
# +0.00000371,
# +0.0001,
# +0.0001097,
# -8500.00062244,
# -6500.00058391,
# -10000.00034496,
# -5000.00020292,
# -7500.00025764,
# -2500.00025741,
# -7500.00022344,
# -6000.00032992,
# -12000.00006886,
# -5000.00006224,
# -16000.00003352,
# -15000.00010019,
# +0.00001,
# -15000.00008735,
# +0.00011314,
# -6000.00013841,
# +0.00000777,
# +47000,
# -500.00023517,
# +20000,
# +5000,
# +25000,
# +50000,
# +36001,
# -0.1334,
# +0.1234,
# +0.01]
#
#
# print(sum(y))
# for a,b in zip(z,y):
#     print(a,b)
#
#
#
# day 1755
# week -3137
# month 58285
# quarter 157987
# half_year 59864
# year -30458
# two_years 534243
# three_years 615994
# five_years 615994
# all_time 615994
#
#
#
# [1, '3-of-7wallet: Huobi-coldwallet', [0,   0,    0,    -10000,     -114051,    -114051,    141452], 225, '35hK24tcLEWcgNA4JxpvbkNkoAcDGqQPsP']
# [2, 'wallet: Binance-coldwallet',     [0,   0,   25604,   43867,      45049,     43538,     118486], 338, '34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo']
# [3, '7wallet: Bitfinex-coldwallet',   [0, -8000, 9000,   51010,       48010,    -68490,     108011], 55, 'bc1qgdjqv0av3q56jvd82tkdjpy7gdp9ut8tlqmgrpmv24sq90ecnvqqjwvw97']
#
#
#
#
#
#
#                 daily           weekly          monthly                 quarter         half_year       year            total
# 3 total ('0(-100.0%)', '-8000(-127.9%)', '34604(-85.6%)', '84877(-84.7%)', '-20992(-103.4%)', '-139003(-117.6%)', '367949(-84.8%)')
# day 0
# week -8000   -8000
# month 34604 '34604(-85.6%)',
# quarter 94877  '84877(-84.7%)',
# half_year -12992 '-20992(-103.4%)',
# year -139003  '-139003(-117.6%)', '
# two_years 296851
# three_years 367948
# five_years 367948
# all_time 367948  367949(-84.8%)
#
#
#
# day 6346
# week 28958
# month 233436
# quarter 487860
# half_year 506816
# year 679941
# two_years 1442506
# three_years 1956220
# five_years 2227497
# all_time 2555019
# day 6346
# week 28958
# month 233436
# quarter 487860
# half_year 506816
# year 679941
# two_years 1442506
# three_years 1956220
# five_years 2227497
# all_time 2555019
# 6075(0.0%)', '28711(0.0%)', '240686(0.0%)', '555272(0.0%)', '612208(0.0%)', '787690(0.0%)', '2413306(0.0%)')
