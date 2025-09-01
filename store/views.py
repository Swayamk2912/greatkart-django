from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import category
from carts.views import _cart_id
from django.http import Http404,HttpResponse
from carts.models import CartItem
from django.core.paginator import Paginator
from django.db.models import Q

def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug:
        categories = get_object_or_404(category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)

    # 🔹 Apply pagination (6 products per page)
    paginator = Paginator(products, 3)  
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'product_count': products.count(),
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Product.DoesNotExist:
        raise Http404("Product not found")

    context = {
        'single_product': single_product,
        'in_cart': in_cart,
    }
    return render(request, 'store/product_detail.html', context)




def search(request):
    products = []
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
    context = {
        'products': products,
        'product_count': len(products),
    }
    return render(request, 'store/store.html', context)

