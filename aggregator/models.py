from django.db import models
from django.utils import timezone
# Create your models here.

class Wallet(models.Model):
    wallet_name = models.TextField(blank=True)
    address = models.TextField()
    misc = models.TextField(blank=True)

    balance = models.TextField()
    delta = models.TextField(default='0')
    transactions_delta =  models.TextField(default='0')
    transactions_delta_all = models.TextField(default='0')
    category = models.TextField(default='normal')

    last_in = models.TextField(blank=True)
    last_out = models.TextField(blank=True)
    in_nums = models.TextField(default='0')
    out_nums = models.TextField(default='0')


    def __str__(self): # to display instance's data when query called
        return self.wallet_name #, self.balance, self.last_in, self.last_out, self.number_of_ins, self.number_of_outs"


class Aggregator(models.Model):

    aggregation_date = models.DateTimeField(default=timezone.now)
    balance = models.TextField(default='0')
    delta = models.TextField(default='0')
    transactions_delta = models.TextField(default='0')
    transactions_delta_all = models.TextField(default='0')
    new_wallets = models.TextField(default='0')
