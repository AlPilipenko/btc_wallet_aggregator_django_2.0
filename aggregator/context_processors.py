from aggregator.models import Wallet_List

def add_variable_to_context(request):
    today_date = Wallet_List.objects.filter(id=1)[0].updated_at
    return {
        'date' : str(today_date)[:10]
    }
