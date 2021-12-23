
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from .models import Product, Category, Favorite
from .forms import SearchForm, HomeSearchForm


def home(request):
    """
    Return Home template
    """
    home_form = HomeSearchForm()
    products = Product.objects.all()
    return render(request, 'catalog/home.html',
                  context = {'home_form': home_form,
                             'products': products})


def products_list(request):
    """
    Allow a user to see a specific products list.
    If his input is empty: return all products from the database.
    If his input matches with a category name: return all products
    from this category.
    If his input matches with products name: return all products
    containing this product name.
    If his input matches with nothing: template will inform user
    that there is no result.
    """
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['search']
            if user_input == '':
                products = Product.objects.all()
            else:
                products = Product.objects.filter(
                    Q(name__icontains=user_input) |
                    Q(categories__name__icontains=user_input)
                )
        products = set(products)
        context = {'user_input': user_input,
                   'products': products, }
    else:
        context = {}
    return render(request, 'catalog/products_list.html', context)


def product_detail(request, product_pk):
    """
    Allow a user to see a product details
    """
    product = get_object_or_404(Product, pk=product_pk)
    return render(request, 'catalog/product_detail.html',
                  context = {'product': product,})


def substitutes_list(request, product_pk):
    """
    Allow a user to see a substitutes list (products with a better nutrition
    grade than the product he chose from a products list)
    """
    product = get_object_or_404(Product, pk=product_pk)
    categories = Category.objects.filter(products__id=product.id)
    substitutes = Product.objects.filter(categories__in=categories,
                                         nutriscore__lt=product.nutriscore)
    substitutes = set(substitutes)
    return render(request, 'catalog/substitutes_list.html',
                  context = {'product': product,
                             'substitutes': substitutes, })


@login_required
def favorite_save(request, product_pk, substitute_pk):
    """
    Allow a logged in user to save a favorite (a substitute with his
    substituted product) to his account from a substitutes list
    """
    product = get_object_or_404(Product, pk=product_pk)
    substitute = get_object_or_404(Product, pk=substitute_pk)
    try:
        favorite = Favorite.objects.create(product=product,
                                           substitute=substitute,
                                           profile=request.user)
        messages.success(
            request, f""""{favorite.substitute.name}" a bien été enregistré"""
        )
    except IntegrityError:
        messages.error(
            request,
            'Ce produit et ce substitut font déjà partie de vos favoris'
        )
    finally:
        return redirect(
            reverse('substitutes_list', kwargs={'product_pk': product.id})
        )


def legal_mentions(request):
    """
    Return legal notice template
    """
    return render(request, 'catalog/legal_mentions.html',
                  context = {})
