
import requests
from django.db.utils import IntegrityError

from catalog.utils.exceptions import RequestResponse404
from catalog.models import Category, Product


class Populate():
    """
    Responsability: Requests Openfoodfacts API in order to
    retrieve some categories and their products.
    Then insert them in database.
    """

    categories_list = []
    """
    Stores categories inserted in database in order know
    which products from wich category have to be inserted
    """

    @classmethod
    def insert_categories(cls, categories_number):
        """
        Insert a list of X categories in database
        from Openfoodfacts categories Json
        """
        request = requests.request(
            "GET", "https://fr.openfoodfacts.org/categories.json"
        )
        if request.status_code == 404:
            raise RequestResponse404
        categories_json = request.json()

        for category in categories_json["tags"]:
            category = Category(name=category["name"])
            cls.categories_list.append(category)
            if len(cls.categories_list) == categories_number:
                break
        Category.objects.bulk_create(cls.categories_list)

    @classmethod
    def is_product_name_valid(cls, product_name):
        """
        Verify that the product name is valid.
        It is only valid if name is not an empty string and:
        - first character is uppercase
          (prevent from names that starts with fr:, en:)
        or
        - first character is a stringified number
          (some names starts with numbers, ex: 100 % pur jus Multifruits)
        """
        if product_name != "":
            if product_name.strip()[0].isupper():
                return True
            elif product_name.strip()[0] in [str(num) for num in range(10)]:
                return True
            else:
                return False
        else:
            return False

    @classmethod
    def nutrients_cleaner(cls, nutrients_dictionary):
        nutrients = {
            'kcal': "",
            'proteins': "",
            'fat': "",
            'saturated_fat': "",
            'carbohydrates': "",
            'sugars': ""
        }
        nutrients['kcal'] = nutrients_dictionary['energy-kcal_100g']
        nutrients['proteins'] = nutrients_dictionary['proteins_100g']
        nutrients['fat'] = nutrients_dictionary['fat_100g']
        nutrients['saturated_fat'] = nutrients_dictionary['saturated-fat_100g']
        nutrients['carbohydrates'] = nutrients_dictionary['carbohydrates_100g']
        nutrients['sugars'] = nutrients_dictionary['sugars_100g']
        return nutrients

    @classmethod
    def insert_products(cls, pages_number):
        """
        Insert X pages of products from each category in database
        Products are inserted with their categories
        """
        for category in cls.categories_list:
            for page in range(pages_number+1):
                request = requests.request(
                    "GET",
                    f"https://fr.openfoodfacts.org/categorie/{category.name}.json/{page}"
                )
                if request.status_code == 404:
                    raise RequestResponse404
                products_json = request.json()

                for product in products_json["products"]:
                    try:
                        if cls.is_product_name_valid(product["product_name_fr"]):
                            try:
                                Product.objects.create(
                                    name=product["product_name_fr"].strip(),
                                    nutriscore=product["nutriscore_grade"].upper(),
                                    nutrients=cls.nutrients_cleaner(product["nutriments"]),
                                    brand=product["brands"],
                                    store=product["stores"],
                                    description=product["generic_name_fr"],
                                    picture=product["image_url"],
                                    url=product["url"]
                                )

                                last_product = Product.objects.latest("id")

                                for cat in product["categories"].split(","):
                                    try:
                                        last_product.categories.add(Category.objects.get(name=cat))
                                    except Category.DoesNotExist:
                                        continue
                                last_product.save()
                            except (KeyError, IntegrityError):
                                continue
                    except KeyError:
                        continue

    @classmethod
    def process(cls, categories_number, pages_number):
        """
        Insert categories and products in database
        """
        cls.insert_categories(categories_number=categories_number)
        cls.insert_products(pages_number=pages_number)
