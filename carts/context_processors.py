from .models import Cart, CartItem
from .views import _cart_id

def counter(request):
    cart_count = 0  # initialize
    if 'admin' in request.path:
        return {}
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # ✅ Only count active items
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0

    # return cart_count to all templates
    return dict(cart_count=cart_count)
