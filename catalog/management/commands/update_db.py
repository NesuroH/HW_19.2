import json
from django.core.management.base import BaseCommand
from catalog.models import Category, Product

class Command(BaseCommand):
    help = 'Очистка базы данных и заполнение новыми данными из JSON-файлов'

    @staticmethod
    def json_read_categories():
        with open('fixtures/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [entry['fields'] for entry in data if entry['model'] == 'catalog.category']

    @staticmethod
    def json_read_products():
        with open('fixtures/data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            return [entry['fields'] for entry in data if entry['model'] == 'catalog.product']

    def handle(self, *args, **options):
        # Удалите все продукты
        Product.objects.all().delete()
        # Удалите все категории
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        categories_for_create = []
        products_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category_data in Command.json_read_categories():
            categories_for_create.append(
                Category(
                    name=category_data['name'],
                    description=category_data.get('description', '')
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(categories_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product_data in Command.json_read_products():
            try:
                category = Category.objects.get(pk=product_data['category'])
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Категория с id '{product_data['category']}' не найдена"))
                continue
            products_for_create.append(
                Product(
                    name=product_data['name'],
                    price=product_data['price'],
                    description=product_data.get('description', ''),
                    category=category
                )
            )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(products_for_create)

        self.stdout.write(self.style.SUCCESS('База данных успешно обновлена'))