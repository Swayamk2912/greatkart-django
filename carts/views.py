from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from store.models import Product
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


# Generate unique cart ID for each session
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    # ✅ Get color and size from query string
    color = request.GET.get('color', 'No color')  
    size = request.GET.get('size', 'No size')  

    # Debugging - only for testing
    # return HttpResponse(f"{color} {size}")

    # ✅ Get the product
    product = get_object_or_404(Product, id=product_id)

    # ✅ Get or create a cart based on session
    try:
        cart_instance = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart_instance = Cart.objects.create(cart_id=_cart_id(request))
        cart_instance.save()

    # ✅ Check if product exists in the cart
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart_instance)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart_instance,
        )
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    cart_instance = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart_instance)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0

    try:
        cart_instance = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart_instance, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
        cart_items = []

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)
