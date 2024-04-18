from django.shortcuts import get_list_or_404, render
from goods.utils import q_serch
from goods.models import Products
from django.core.paginator import Paginator


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    query = request.GET.get('q', None)
    

    if category_slug == "all":
        goods = Products.objects.all()
    elif query:
        goods = q_serch(query)
        
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    paginator = Paginator(goods, 3)

    current_page = paginator.page(int(page))

    context ={ 
        "title" : "Каталог",
        "goods" : current_page,
    }
    return render(request, 'goods/catalog.html', context)

def product(request, product_slug):

    product = Products.objects.get(slug=product_slug)

    goods = Products.objects.all()

    paginator = Paginator(goods, 3)
    current_page = paginator.page(1)

    context ={ 
        "title" : "Каталог",
        "product" : product,
         "goods" : current_page,
    }
    return render(request, 'goods/product.html', context)
