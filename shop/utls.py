from decimal import Decimal

def total(cart_items):
    total_price = Decimal('0.00')
    for item in cart_items:
        price = Decimal(str(item['data']['price']))
        quantity = int(item['quantity'])
        total_price += price * quantity
    return total_price