from django.db import models

# Create your models here.

class Wallet(models.Model):
    wallet_name = models.TextField(blank=True)
    address = models.TextField()
    balance = models.TextField()
    misc = models.TextField(blank=True)
    last_in = models.TextField(blank=True)
    last_out = models.TextField(blank=True)
    in_nums = models.TextField(blank=True)
    out_nums = models.TextField(blank=True)
    category = models.TextField(default='normal')
    up_to_date = models.TextField(default='no')
    transactions_delta =  models.TextField(default='[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]')

    def __str__(self): # to display instance's data when query called
        return self.wallet_name #, self.balance, self.last_in, self.last_out, self.number_of_ins, self.number_of_outs"
