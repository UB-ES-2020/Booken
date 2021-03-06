#  deepcode ignore C0411: not an issue
import base64
import json
import unittest
#  deepcode ignore C0411: not an issue
import sys
#  deepcode ignore C0411: not an issue
import random



sys.path.append('../')
#  deepcode ignore C0413: stupid issue
from app import setupApp
#  deepcode ignore C0413: stupid issue
from db import db
from models.accounts import AccountModel

#  deepcode ignore C0411: not an issue


class SearchBookTests(unittest.TestCase):
    account_admin_info = {
        "name": 'Admin',
        "lastname": 'Admin',
        "email": "a@a.com",
        "password": 'sm22'
    }
    book_info1 = {
        "isbn": 12345678911,
        "name": 'The secret of the Stones',
        "author_name": 'Kim Follet',
        "author_bd": '10/10/1979',
        "author_city": "BCN",
        "author_country": "Spain",
        "genre": 'HUMANIDADES',
        "year": 2020,
        "editorial": 'Santillana',
        "language": 'Castellano',
        "price": 10.9,
        "synopsis": 'Synopsis',
        "description": 'Descripcion',
        "num_pages": 130,
        "cover_type": 0,
        "num_sales": 0,
        "total_available": 15,
        "cover_image_url": 'asd',
        "back_cover_image_url": 'asd'
    }

    def setUp(self):
        self.app = setupApp(True).test_client()
        db.drop_all()
        db.create_all()
        self.register(self.account_admin_info)
        self.acc = AccountModel.find_by_email("a@a.com")
        self.acc.type = 2
        self.acc.save_to_db()
        self.resp_account_admin = self.login('a@a.com', 'sm22')
        self.authorization = {'Authorization': 'Basic ' + base64.b64encode(
            bytes(
                str(self.acc.id) + ":" + json.loads(self.resp_account_admin.data)['token'],
                'ascii')).decode(
            'ascii')}

    def tearDown(self):
        # Executed after each test
        pass

    def test_search_by_name(self):
        self.postBook(self.book_info1)
        lista = ['the', 'sec', 'secret', 'of', 'stones']
        rand = random.choices(lista)
        response = self.search(rand)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'The secret of the Stones', response.data)

    def test_search_by_isbn(self):
        self.postBook(self.book_info1)
        lista = [12, 123, 567, 123456789]
        rand = random.choices(lista)
        response = self.search(rand)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'12345678911', response.data)
        self.assertIn(b'The secret of the Stones', response.data)

    def test_search_by_author_name(self):
        self.postBook(self.book_info1)
        lista = ['kim', 'foll', 'follet']
        response = self.search(random.choices(lista))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Kim Follet', response.data)
        self.assertIn(b'The secret of the Stones', response.data)

    def postBook(self, info):
        return self.app.post('api/book',
                             data=info,
                             headers=self.authorization,
                             follow_redirects=True)

    def search(self, name):
        return self.app.get('api/search', data={'name': name}, follow_redirects=True)

    def register(self, info):
        return self.app.post('api/account',
                             data=info,
                             follow_redirects=True)

    def login(self, email, password):
        return self.app.post('api/login',
                             data=dict(email=email, password=password),
                             follow_redirects=True)
