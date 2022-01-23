
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Product, Category, Favorite
from .forms import SearchForm, HomeSearchForm


def home(request):
    """
    Return Home template
    """
    home_form = HomeSearchForm()
    return render(request, 'catalog/home.html', {'home_form': home_form})


def search_product(request):
    user_input = request.GET.get('query', default='')
    payload = []
    if user_input:
        products = Product.objects.filter(
            Q(name__icontains=user_input) |
            Q(categories__name__icontains=user_input)
        ).distinct().order_by('-nutriscore')

        for product in products:
            payload.append(product.name)

    return JsonResponse({'data': payload})


def get_user_input(request):
    """
    Get the user input from search forms and redirects to the
    correct view in terms of the input is empty or not.
    It avoids an issue with pagination when this algorithm is
    in the view.
    """
    user_input = request.GET.get('query', default='')
    if user_input == '':
        return redirect(
            reverse('all_products_list')
        )
    else:
        return redirect(
            reverse('products_list', kwargs={'user_input': user_input})
        )


def products_list(request, user_input):
    """
    Allow a user to see a specific products list.
    If his input matches with a category name: return all products
    from this category.
    If his input matches with products name: return all products
    containing this product name.
    If his input matches with nothing: template will inform user
    that there is no result.
    """
    products = Product.objects.filter(
            Q(name__icontains=user_input) |
            Q(categories__name__icontains=user_input)
    ).distinct().order_by('-nutriscore')

    p = Paginator(products, 60)
    page_number = request.GET.get('page')
    try:
        products = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        products = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        products = p.page(p.num_pages)
    return render(request, 'catalog/products_list.html', {'user_input': user_input, 'products': products})


def all_products_list(request):
    """
    Display all database products
    """
    products = Product.objects.all().order_by('-nutriscore')

    p = Paginator(products, 60)
    page_number = request.GET.get('page')
    try:
        products = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        products = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        products = p.page(p.num_pages)
    return render(
        request, 'catalog/products_list.html', {'products': products}
    )


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
    substitutes = Product.objects.filter(
        categories__in=categories,
        nutriscore__lt=product.nutriscore
    ).distinct().order_by('nutriscore')

    p = Paginator(substitutes, 6)
    page_number = request.GET.get('page')
    try:
        substitutes = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        substitutes = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        substitutes = p.page(p.num_pages)
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
