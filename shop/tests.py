from unittest import mock
from django.urls import reverse_lazy, reverse
from rest_framework.test import APITestCase

from shop.models import Category, Product

# import du mock avec la valeur attendue de l'ecoscore 
from shop.mocks import mock_openfoodfact_success, ECOSCORE_GRADE 

class ShopAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='Fruits', active=True)
        Category.objects.create(name='Légumes', active=False)

        cls.product = cls.category.products.create(name='Ananas', active=True)
        cls.category.products.create(name='Banane', active=False)

        cls.category_2 = Category.objects.create(name='Légumes', active=True)
        cls.product_2 = cls.category_2.products.create(name='Tomate', active=True)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_article_list_data(self, articles):
        return [
            {
                'id': article.pk,
                'name': article.name,
                'date_created': self.format_datetime(article.date_created),
                'date_updated': self.format_datetime(article.date_updated),
                'product': article.product_id
            } for article in articles
        ]

    def get_product_list_data(self, products):
        return [
            {
                'id': product.pk,
                'name': product.name,
                'date_created': self.format_datetime(product.date_created),
                'date_updated': self.format_datetime(product.date_updated),
                'category': product.category_id,
                'ecoscore': ECOSCORE_GRADE  # la valeur de l'ecoscore provient de notre constante utilisée dans notre mock
            } for product in products
        ]

    def get_category_list_data(self, categories):
        return [
            {
               'id': category.id,
                'name': category.name,
                'description': category.description,
                'date_created': self.format_datetime(category.date_created),
                'date_updated': self.format_datetime(category.date_updated),
            } for category in categories
        ]

class TestCategory(ShopAPITestCase):

    # Nous stockons l’url de l'endpoint dans un attribut de classe pour pouvoir l’utiliser plus facilement dans chacun de nos tests
    # reverse_lazy : 'category-list' : completude faite par le router
    url = reverse_lazy('category-list')

    # TEST L'ENDPOINT
    # On réalise l’appel en GET en utilisant le client de la classe de test
    # response = self.client.get(self.url)
    # Nous vérifions que le status code est bien 200
    # et que les valeurs retournées sont bien celles attendues : self.assertEqual(response.status_code, 200)
    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # expected = [
        #     {
        #         'id': category.id,
        #         'name': category.name,
        #         'date_created': self.format_datetime(category.date_created),
        #         'date_updated': self.format_datetime(category.date_updated),
        #     } for category in [self.category, self.category_2]
        # ]
        self.assertEqual(response.json(), self.get_category_list_data([self.category, self.category_2]))

    # def test_detail(self):
    # # Nous utilisons l'url de détail
    #     url_detail = reverse('category-detail',kwargs={'pk': self.category.pk})
    #     response = self.client.get(url_detail)
    #     # Nous vérifions également le status code de retour ainsi que les données reçues
    #     self.assertEqual(response.status_code, 200)
    #     excepted = {
    #         'id': self.category.pk,
    #         'name': self.category.name,
    #         'date_created': self.format_datetime(self.category.date_created),
    #         'date_updated': self.format_datetime(self.category.date_updated),
    #         'products': self.get_product_detail_data(self.category.products.filter(active=True)),
    #     }
    #     self.assertEqual(excepted, response.json())

    # deuxieme test pour verifier que la creation n'est pas possible
    def test_create(self):
        # Nous vérifions qu’aucune catégorie n'existe avant de tenter d’en créer une
        # self.assertFalse(Category.objects.exists())
        category_count = Category.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        # Vérifions que le status code est bien en erreur et nous empêche de créer une catégorie
        self.assertEqual(response.status_code, 405)
        # Enfin, vérifions qu'aucune nouvelle catégorie n’a été créée malgré le status code 405
        self.assertEqual(Category.objects.count(), category_count)

#pk: primary key

class TestProduct(ShopAPITestCase):

    url = reverse_lazy('product-list')

    # teste l'endpoint
    @mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
    # Le premier paramètre est la méthode à mocker
    # Le second est le mock à appliquer
    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_list_data([self.product, self.product_2]), response.json())

    # teste l'endpoint avec filtre
    @mock.patch('shop.models.Product.call_external_api', mock_openfoodfact_success)
    # Le premier paramètre est la méthode à mocker
    # Le second est le mock à appliquer
    def test_list_filter(self):
        response = self.client.get(self.url + '?category_id=%i' % self.category.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.get_product_list_data([self.product]), response.json())

    # tente de creer un produit / ne doit pas marcher
    # 405 : method not allowed
    def test_create(self):
        product_count = Product.objects.count()
        response = self.client.post(self.url, data={'name': 'Nouvelle catégorie'})
        self.assertEqual(response.status_code, 405)
        self.assertEqual(Product.objects.count(), product_count)

    # tente de delte / ne doit pas marcher
    # 405 : method not allowed
    def test_delete(self):
        response = self.client.delete(reverse('product-detail', kwargs={'pk': self.product.pk}))
        self.assertEqual(response.status_code, 405)
        self.product.refresh_from_db()

    # def test_detail(self):
    #     response = self.client.get(reverse('product-detail', kwargs={'pk': self.product.pk}))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(self.get_product_detail_data(self.product), response.json())