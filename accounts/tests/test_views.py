
from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import Profile
from catalog.models import Product, Favorite


class SignupViewTest(TestCase):

    def test_signup_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_view_url_accessible_by_name(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_view_uses_correct_template(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'accounts/registration/signup.html')


class LoginViewTest(TestCase):

    def setUp(self):
        Profile.objects.create(username='usertest',
                               email='usertest@gmail.com',
                               password='m0t2passe')

    def test_login_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/registration/login.html')


class AccountViewTest(TestCase):

    def setUp(self):
        user = Profile.objects.create(username='vanrussom',
                                      email='vanrussom@django.com')
        user.set_password('Django56789')
        user.save()

    def test_account_view_redirects_if_user_not_logged(self):
        response = self.client.get('/accounts/account/')
        self.assertRedirects(
            response, '/accounts/login/?next=/accounts/account/'
        )

    def test_account_view_when_user_logged(self):
        self.client.login(email='vanrussom@django.com', password='Django56789')
        response = self.client.get('/accounts/account/')
        self.assertEqual(response.status_code, 200)

    def test_account_view_url_accessible_by_name(self):
        self.client.login(email='vanrussom@django.com', password='Django56789')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)

    def test_account_view_uses_correct_template(self):
        self.client.login(email='vanrussom@django.com', password='Django56789')
        response = self.client.get(reverse('account'))
        self.assertTemplateUsed(response, 'accounts/account.html')


class FavoritesListViewTest(TestCase):

    def setUp(self):
        nutella = Product.objects.create(
            name='Nutella',
            nutriscore='D',
            url='https://fr.openfoodfacts.org/produit/47647/Nutella'
        )

        nocciolata = Product.objects.create(
            name='Nocciolata',
            nutriscore='C',
            url='https://fr.openfoodfacts.org/produit/183647/Nocciolata'
        )

        milka = Product.objects.create(
            name='Milka à tartiner',
            nutriscore='B',
            url='https://fr.openfoodfacts.org/produit/148109/Milka'
        )

        daim = Product.objects.create(
            name='Daim à tartiner',
            nutriscore='C',
            url='https://fr.openfoodfacts.org/produit/813619/Daim'
        )

        user = Profile.objects.create(username='vanrussom',
                                      email='vanrussom@django.com')
        user.set_password('Django56789')
        user.save()

        Favorite.objects.create(product=nutella,
                                substitute=nocciolata,
                                profile=user)
        Favorite.objects.create(product=nocciolata,
                                substitute=milka,
                                profile=user)
        Favorite.objects.create(product=daim,
                                substitute=milka,
                                profile=user)
        Favorite.objects.create(product=nutella,
                                substitute=daim,
                                profile=user)

    def test_favorites_list_view_redirects_if_user_not_logged(self):
        response = self.client.get('/accounts/favorites/')
        self.assertRedirects(response,
                             '/accounts/login/?next=/accounts/favorites/')

    def test_favorites_list_view_when_user_logged(self):
        self.client.login(email='vanrussom@django.com', password='Django56789')
        response = self.client.get(reverse('favorites'))
        # Check user is logged in
        self.assertEqual(str(response.context['profile'].username),
                         'vanrussom')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check if favorites in context
        self.assertEqual(len(response.context['favorites']), 4)
        # Check we used correct template
        self.assertTemplateUsed(response, 'accounts/favorites_list.html')


class FavoriteDetailViewTest(TestCase):

    def setUp(self):
        nutella = Product.objects.create(
            name='Nutella',
            nutriscore='D',
            url='https://fr.openfoodfacts.org/produit/47647/Nutella'
        )

        nocciolata = Product.objects.create(
            name='Nocciolata',
            nutriscore='C',
            url='https://fr.openfoodfacts.org/produit/183647/Nocciolata'
        )

        user = Profile.objects.create(username='vanrussom',
                                      email='vanrussom@django.com')
        user.set_password('Django56789')
        user.save()

        Favorite.objects.create(product=nutella,
                                substitute=nocciolata,
                                profile=user)

    def test_favorite_detail_view_redirects_if_user_not_logged(self):
        favorite = Favorite.objects.all().first()
        response = self.client.get(f'/accounts/favorite/{favorite.id}/')
        self.assertRedirects(
            response,
            f'/accounts/login/?next=/accounts/favorite/{favorite.id}/'
        )

    def test_favorite_detail_view_when_user_logged(self):
        user = Profile.objects.get(username='vanrussom')
        self.client.login(email='vanrussom@django.com', password='Django56789')
        favorite = user.favorite_set.all().first()
        response = self.client.get(f'/accounts/favorite/{favorite.id}/')
        # Check user is logged in
        self.assertEqual(str(response.context['user'].username), 'vanrussom')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # # Check if favorites in context
        self.assertEqual(response.context['favorite'].id, favorite.id)
        # # Check we used correct template
        self.assertTemplateUsed(response, 'accounts/favorite_detail.html')


class DeleteFavoriteViewTest(TestCase):

    def setUp(self):
        nutella = Product.objects.create(
            name='Nutella',
            nutriscore='D',
            url='https://fr.openfoodfacts.org/produit/47647/Nutella'
        )

        nocciolata = Product.objects.create(
            name='Nocciolata',
            nutriscore='C',
            url='https://fr.openfoodfacts.org/produit/183647/Nocciolata'
        )

        user = Profile.objects.create(username='vanrussom',
                                      email='vanrussom@django.com')
        user.set_password('Django56789')
        user.save()

        Favorite.objects.create(product=nutella,
                                substitute=nocciolata,
                                profile=user)

    def test_delete_favorite_view(self):
        self.client.login(email='vanrussom@django.com', password='Django56789')
        favorite = Favorite.objects.all().first()
        response = self.client.post(
            f'/accounts/favorite/{favorite.id}/delete/'
        )
        self.assertRedirects(response, '/accounts/favorites/')
        # favorite has been deleted
        with self.assertRaises(ObjectDoesNotExist):
            Favorite.objects.get(id=favorite.id)
