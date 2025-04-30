from shop.models import *

def sync_cart_to_db(request, user):
    cart_data = request.session.get('cart', {})

    if not cart_data:
        return
    cart, created = Cart.objects.get_or_create(user=user)

    CartItem.objects.filter(cart=cart).delete()
    for key, value in cart_data.items():
        item_type, item_id = key.split('_')
        if item_type == 'product':
            obj = Product.objects.get(id=item_id)
        elif item_type == 'box':
            obj = Box.objects.get(id=item_id)
        else:
            continue 
        CartItem.objects.create(
            cart=cart,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
            quantity=value['quantity']
        )
    del request.session['cart']
