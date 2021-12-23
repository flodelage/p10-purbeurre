
from django.core.management.base import BaseCommand

from catalog.utils.populate import Populate


class Command(BaseCommand):
    """
    Command that calls Populate.process() method in order to
    populate the database with some Openfoodfacts' data.
    """

    help = "Populates database with some Openfoodfacts' data"

    def handle(self, *args, **kwargs):
        Populate.process(categories_number=50, pages_number=8)
