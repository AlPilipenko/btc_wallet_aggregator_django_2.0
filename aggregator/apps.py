from django.apps import AppConfig
import os

class AggregatorConfig(AppConfig):
    name = 'aggregator'

    """ bitinfocharts.com displays lists of 100 bitcoin wallets per page.
        There are 100 pages, hence 10 000 wallets to analyse.
    """

    PAGE_SEARCH_RANGE =  1, 11 # max range(1-100)
    START_PAGE = 1 # Wallet position where to start search (1-100)
    WALLET_SEARCH_END_POSITION = 100 # in case of debbuging wallets (1-100)
