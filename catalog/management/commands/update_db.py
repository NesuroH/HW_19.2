import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Fill the database with data from JSON files'

    @staticmethod
    def json_read_categories():
        with open('fixtures/category_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def json_read_products():
        with open('fixtures/product_data.json', 'r', encoding='utf-8') as file:
            return json.load(file)

    def handle(self, *args, **options):
        # Удалите все продукты
        Product.objects.all().delete()
        # Удалите все категории
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        category_for_create = []
        product_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category_data in Command.json_read_categories():
            fields = category_data['fields']
            category_for_create.append(
                Category(id=category_data['pk'], name=fields['name'], description=fields['description'])
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product_data in Command.json_read_products():
            fields = product_data['fields']
            product_for_create.append(
                Product(
                    id=product_data['pk'],
                    name=fields['name'],
                    description=fields['description'],
                    price=fields['price'],
                    category=Category.objects.get(pk=fields['category']),
                    created_at=fields.get('created_at', None),
                    updated_at=fields.get('updated_at', None)
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(self.style.SUCCESS('Database successfully filled with new data'))