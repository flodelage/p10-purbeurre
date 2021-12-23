
from django.test import TestCase
from django.urls import reverse

from catalog.models import Product, Category
from accounts.models import Profile


class HomeViewTest(TestCase):

    def test_home_view_url_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'catalog/home.html')


class ProductsListViewTest(TestCase):

    def test_products_list_view_url_exists_at_desired_location_get_request(self):
        response = self.client.get('/catalog/products/')
        self.assertEqual(response.status_code, 200)

    def test_products_list_view_url_exists_at_desired_location_post_request(self):
        response = self.client.post('/catalog/products/')
        self.assertEqual(response.status_code, 200)

    def test_products_list_view_url_accessible_by_name(self):
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)

    def test_products_list_view_uses_correct_template(self):
        response = self.client.get(reverse('products_list'))
        self.assertTemplateUsed(response, 'catalog/products_list.html')


class ProductDetailView(TestCase):

    def setUp(self):
        Product.objects.create(
            name='Nutella',
            nutriscore='D',
            url='https://fr.openfoodfacts.org/produit/47647/Nutella'
        )

    def test_product_detail_view_url_exists_at_desired_location(self):
        product = Product.objects.get(name='Nutella')
        response = self.client.get(f'/catalog/product/{product.id}/')
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_url_accessible_by_name(self):
        product = Product.objects.get(name='Nutella')
        response = self.client.get(reverse('product_detail',
                                           kwargs={'product_pk': product.id}))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view_uses_correct_template(self):
        product = Product.objects.get(name='Nutella')
        response = self.client.get(reverse('product_detail',
                                           kwargs={'product_pk': product.id}))
        self.assertTemplateUsed(response, 'catalog/product_detail.html')


class SubstitutesListView(TestCase):

    def setUp(self):
        category = Category.objects.create(name='Pate à tartiner')

        nutella = Product.objects.create(
            name='Nutella',
            nutriscore='D',
            url='https://fr.openfoodfacts.org/produit/47647/Nutella',
        )
        nutella.categories.add(category)

        nocciolata = Product.objects.create(
            name='Nocciolata',
            nutriscore='C',
            url='https://fr.openfoodfacts.org/produit/183647/Nocciolata'
        )
        nocciolata.categories.add(category)

        milka = Product.objects.create(
            name='Milka à tartiner',
            nutriscore='B',
            url='https://fr.openfoodfacts.org/produit/148109/Milka'
        )
        milka.categories.add(category)

        daim = Product.objects.create(
            name='Daim à tartiner',
            nutriscore='C',
            url='https://fr.openfoodfacts.org/produit/813619/Daim'
        )
        daim.categories.add(category)

    def test_substitutes_list_view_url_exists_at_desired_location(self):
        product = Product.objects.get(name='Nutella')
        response = self.client.get(f'/catalog/product/{product.id}/substitutes/')
        self.assertEqual(response.status_code, 200)

    def test_substitutes_list_view_url_accessible_by_name(self):
        product = Product.objects.get(name='Nutella')
        response = self.client.get(reverse('substitutes_list',
                                           kwargs={'product_pk': product.id}))
        self.assertEqual(response.status_code, 200)

    def test_substitutes_list_view_uses_correct_template(self):
        product = Product.objects.get(name='Nutella')
        response = self.client.get(reverse('substitutes_list',
                                           kwargs={'product_pk': product.id}))
        self.assertTemplateUsed(response, 'catalog/substitutes_list.html')

    def test_substitutes_list_view_product_in_context(self):
        product = Product.objects.get(name='Nutella')
        response = self.client.get(f'/catalog/product/{product.id}/substitutes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['product'], product)

    def test_substitutes_list_view_substitutes_in_context(self):
        product = Product.objects.get(name='Nutella')
        response = self.client.get(f'/catalog/product/{product.id}/substitutes/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['substitutes']), 3)


class FavoriteSave(TestCase):

    def setUp(self):
        Product.objects.create(
            name='Nutella',
            nutriscore='D',
            url='https://fr.openfoodfacts.org/produit/47647/Nutella',
        )

        Product.objects.create(
            name='Nocciolata',
            nutriscore='C',
            url='https://fr.openfoodfacts.org/produit/183647/Nocciolata'
        )

        user = Profile.objects.create(username='vanrussom',
                                      email='vanrussom@django.com')
        user.set_password('Django56789')
        user.save()

    def test_favorite_save_view_post_request_redirection_url_when_user_not_logged(self):
        product = Product.objects.get(name='Nutella')
        substitute = Product.objects.get(name='Nocciolata')
        response = self.client.post(
            f'/catalog/favorite_save/product/{product.id}/substitute/{substitute.id}/'
        )
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/catalog/favorite_save/product/{product.id}/substitute/{substitute.id}/'
        )

    def test_favorite_save_view_post_request_redirection_url_when_user_logged(self):
        self.client.login(email='vanrussom@django.com', password='Django56789')
        product = Product.objects.get(name='Nutella')
        substitute = Product.objects.get(name='Nocciolata')
        response = self.client.post(
            f'/catalog/favorite_save/product/{product.id}/substitute/{substitute.id}/'
        )
        self.assertRedirects(response,
                             f'/catalog/product/{product.id}/substitutes/')


class LegalMentions(TestCase):

    def test_legal_mentions_view_url_exists_at_desired_location(self):
        response = self.client.get('/legal_mentions/')
        self.assertEqual(response.status_code, 200)

    def test_legal_mentions_view_url_accessible_by_name(self):
        response = self.client.get(reverse('legal_mentions'))
        self.assertEqual(response.status_code, 200)

    def test_legal_mentions_view_uses_correct_template(self):
        response = self.client.get(reverse('legal_mentions'))
        self.assertTemplateUsed(response, 'catalog/legal_mentions.html')
