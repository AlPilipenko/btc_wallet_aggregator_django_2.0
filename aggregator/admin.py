from django.contrib import admin

# Register your models here.

from .models import Wallet
admin.site.register(Wallet)

from .models import Wallet_List
admin.site.register(Wallet_List)

from .models import Aggregator
admin.site.register(Aggregator)

from .models import Category
admin.site.register(Category)
