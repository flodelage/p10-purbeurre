
from django.test import TestCase

from catalog.models import Category, Product, Favorite
from accounts.models import Profile


class CategoryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cat = Category.objects.create(name='categorie de test')

        nutella = Product.objects.create(
            name='Nutella',
            nutriscore='D',
            nutrients={
                'kcal': "300",
                'proteins': "23",
                'fat': "12",
                'saturated_fat': "10",
                'carbohydrates': "35",
                'sugars': "20"
            },
            brand='Ferrero',
            description='huile de palme',
            store='Auchan, Carrefour',
            picture='https://static.openfoodfacts.org/images/products/47647.jpg',
            url='https://fr.openfoodfacts.org/produit/47647/Nutella'
        )

        nocciolata = Product.objects.create(
            name='Nocciolata',
            nutriscore='C',
            nutrients={
                'kcal': "250",
                'proteins': "12",
                'fat': "20",
                'saturated_fat': "14",
                'carbohydrates': "35",
                'sugars': "17"
            },
            brand='Rigoni di Asiago',
            description='bio, sans huile de palme',
            store='Leclerc',
            picture='https://static.openfoodfacts.org/images/products/183647.jpg',
            url='https://fr.openfoodfacts.org/produit/183647/Nocciolata'
        )

        nutella.categories.add(cat)
        nocciolata.categories.add(cat)

    def test_name(self):
        category = Category.objects.get(name='categorie de test')
        name = category.name
        self.assertEquals(name, 'categorie de test')

    def test_name_max_length(self):
        category = Category.objects.get(name='categorie de test')
        max_length = category._meta.get_field('name').max_length
        self.assertEquals(max_length, 254)

    def test_name_unique(self):
        category = Category.objects.get(name='categorie de test')
        unique = category._meta.get_field('name').unique
        self.assertEquals(unique, True)

    def test_object_str(self):
        category = Category.objects.get(name='categorie de test')
        object_str = category.__str__()
        self.assertEquals(
            object_str,
            f"Catégorie {category.pk}: {category.name}"
        )

    def test_products(self):
        category = Category.objects.get(name='categorie de test')
        products = [p.name for p in category.products.all()]
        self.assertEquals(sorted(products), ['Nocciolata', 'Nutella'])


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        snacks = Category.objects.create(name='snacks')
        desserts = Category.objects.create(name='desserts')

        p = Product.objects.create(
            name='produit de test',
            nutriscore='C',
            nutrients={
                'kcal': "250",
                'proteins': "12",
                'fat': "20",
                'saturated_fat': "14",
                'carbohydrates': "35",
                'sugars': "17"
            },
            brand='Nestlé',
            description='produit sans gluten',
            store='Auchan, Carrefour',
            picture='https://static.openfoodfacts.org/images/products/1234.jpg',
            url='https://fr.openfoodfacts.org/produit/1234/produit_de_test'
        )

        p.categories.add(snacks, desserts)

    def test_name(self):
        product = Product.objects.get(name='produit de test')
        name = product.name
        self.assertEquals(name, 'produit de test')

    def test_name_unique(self):
        product = Product.objects.get(name='produit de test')
        unique = product._meta.get_field('name').unique
        self.assertEquals(unique, True)

    def test_name_max_length(self):
        product = Product.objects.get(name='produit de test')
        max_length = product._meta.get_field('name').max_length
        self.assertEquals(max_length, 254)

    def test_nutriscore(self):
        product = Product.objects.get(name='produit de test')
        nutriscore = product.nutriscore
        self.assertEquals(nutriscore, 'C')

    def test_nutriscore_max_length(self):
        product = Product.objects.get(name='produit de test')
        max_length = product._meta.get_field('nutriscore').max_length
        self.assertEquals(max_length, 1)

    def test_nutrients(self):
        product = Product.objects.get(name='produit de test')
        nutrients = product.nutrients
        expected_result = {
            'kcal': "250",
            'proteins': "12",
            'fat': "20",
            'saturated_fat': "14",
            'carbohydrates': "35",
            'sugars': "17"
        }
        self.assertEquals(nutrients, expected_result)

    def test_brand(self):
        product = Product.objects.get(name='produit de test')
        brand = product.brand
        self.assertEquals(brand, 'Nestlé')

    def test_brand_max_length(self):
        product = Product.objects.get(name='produit de test')
        max_length = product._meta.get_field('brand').max_length
        self.assertEquals(max_length, 254)

    def test_brand_null(self):
        product = Product.objects.get(name='produit de test')
        null = product._meta.get_field('brand').null
        self.assertEquals(null, True)

    def test_description(self):
        product = Product.objects.get(name='produit de test')
        description = product.description
        self.assertEquals(description, 'produit sans gluten')

    def test_description_null(self):
        product = Product.objects.get(name='produit de test')
        null = product._meta.get_field('description').null
        self.assertEquals(null, True)

    def test_store(self):
        product = Product.objects.get(name='produit de test')
        store = product.store
        self.assertEquals(store, 'Auchan, Carrefour')

    def test_store_max_length(self):
        product = Product.objects.get(name='produit de test')
        max_length = product._meta.get_field('store').max_length
        self.assertEquals(max_length, 254)

    def test_store_null(self):
        product = Product.objects.get(name='produit de test')
        null = product._meta.get_field('store').null
        self.assertEquals(null, True)

    def test_picture(self):
        product = Product.objects.get(name='produit de test')
        picture = product.picture
        self.assertEquals(picture, 'https://static.openfoodfacts.org/images/products/1234.jpg')

    def test_picture_null(self):
        product = Product.objects.get(name='produit de test')
        null = product._meta.get_field('picture').null
        self.assertEquals(null, True)

    def test_url(self):
        product = Product.objects.get(name='produit de test')
        url = product.url
        self.assertEquals(url, 'https://fr.openfoodfacts.org/produit/1234/produit_de_test')

    def test_object_str(self):
        product = Product.objects.get(name='produit de test')
        object_str = product.__str__()
        self.assertEquals(
            object_str,
            f"""Produit {product.pk}: {product.name} / Nutriscore: {product.nutriscore} / Marque(s): {product.brand} / Url: {product.url}"""
        )

    def test_categories(self):
        product = Product.objects.get(name='produit de test')
        categories = [cat.name for cat in product.categories.all()]
        self.assertEquals(sorted(categories), ['desserts', 'snacks'])


class SomeFavoriteTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        Product.objects.create(
            name='Nutella',
            nutriscore='D',
            nutrients={
                'kcal': "300",
                'proteins': "23",
                'fat': "12",
                'saturated_fat': "10",
                'carbohydrates': "35",
                'sugars': "20"
            },
            brand='Ferrero',
            description='huile de palme',
            store='Auchan, Carrefour',
            picture='https://static.openfoodfacts.org/images/products/47647.jpg',
            url='https://fr.openfoodfacts.org/produit/47647/Nutella'
        )

        Product.objects.create(
            name='Nocciolata',
            nutriscore='C',
            nutrients={
                'kcal': "250",
                'proteins': "12",
                'fat': "20",
                'saturated_fat': "14",
                'carbohydrates': "35",
                'sugars': "17"
            },
            brand='Rigoni di Asiago',
            description='bio, sans huile de palme',
            store='Leclerc',
            picture='https://static.openfoodfacts.org/images/products/183647.jpg',
            url='https://fr.openfoodfacts.org/produit/183647/Nocciolata'
        )

        Profile.objects.create(username='vanrussom',
                               email='vanrussom@django.com',
                               password='Django56789')

    def test_product(self):
        product = Product.objects.get(name='Nutella')
        substitute = Product.objects.get(name='Nocciolata')
        profile = Profile.objects.get(username='vanrussom')
        favorite = Favorite.objects.create(product=product,
                                           substitute=substitute,
                                           profile=profile)
        self.assertEquals(product, favorite.product)

    def test_substitute(self):
        product = Product.objects.get(name='Nutella')
        substitute = Product.objects.get(name='Nocciolata')
        profile = Profile.objects.get(username='vanrussom')
        favorite = Favorite.objects.create(product=product,
                                           substitute=substitute,
                                           profile=profile)
        self.assertEquals(substitute, favorite.substitute)

    def test_profile(self):
        product = Product.objects.get(name='Nutella')
        substitute = Product.objects.get(name='Nocciolata')
        profile = Profile.objects.get(username='vanrussom')
        favorite = Favorite.objects.create(product=product,
                                           substitute=substitute,
                                           profile=profile)
        self.assertEquals(profile, favorite.profile)

    def test_unique_together(self):
        product = Product.objects.get(name='Nutella')
        substitute = Product.objects.get(name='Nocciolata')
        profile = Profile.objects.get(username='vanrussom')
        favorite = Favorite.objects.create(product=product,
                                           substitute=substitute,
                                           profile=profile)
        unique_together = (('substitute', 'product', 'profile'),)
        self.assertEquals(unique_together, favorite._meta.unique_together)

    def test_object_str(self):
        product = Product.objects.get(name='Nutella')
        substitute = Product.objects.get(name='Nocciolata')
        profile = Profile.objects.get(username='vanrussom')
        favorite = Favorite.objects.create(product=product,
                                           substitute=substitute,
                                           profile=profile)
        object_str = favorite.__str__()
        self.assertEquals(object_str, f"Favori {favorite.pk}: Substitut: {favorite.substitute} / Produit substitué: {favorite.product} / {favorite.profile}")
