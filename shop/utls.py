

def total(data):
    total_price=0
    for i in data:
        total_price+=i['data']['price'] * i['quantity']
    return total_price