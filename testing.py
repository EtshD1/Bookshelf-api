import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db


class APITestCase(unittest.TestCase):
    """This class represents the resource test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}@{}/{}".format(
            'etsh:3894',
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_book = {
            'name': 'etsh',
            'author': 'etsh'
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    def test_get_paginated_books(self):
        res = self.client().get('/books')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

    def test_404_sent_reqesting_beyond_valid_page(self):
        res = self.client().get('/books?page=10000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    def test_post_new_book(self):
        jsonData = {'name': 'Whisper', 'author': 'Hesham'}
        res = self.client().post(
            '/books', json=jsonData)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['book'])
        self.assertEqual(data['book']['name'], jsonData['name'])
        self.assertEqual(data['book']['author'], jsonData['author'])

    def test_delete_book(self):
        id = 5
        res = self.client().delete(f'/books/{id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['total_books'])
        self.assertEqual(data['deleted_book_id'], id)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
