
from django.core.management.base import BaseCommand
from django.core import management
from django.db import connection


class Command(BaseCommand):
    """
    Command that drops current database.
    """

    help = "Drop current database"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
        management.call_command('migrate')
