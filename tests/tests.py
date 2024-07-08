import unittest
from flask_testing import TestCase
from management_system.app import app, db
from management_system.models import Book, Review

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_book(self):
        response = self.client.post('/books', json={
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'year_published': 2020,
            'summary': 'Test Summary'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Book added successfully', response.json['message'])

    def test_get_all_books(self):
        response = self.client.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_book_summary_valid_id(self):
        book = Book(title='Test Book', author='Test Author', genre='Test Genre', year_published=2020, summary='Test Summary')
        db.session.add(book)
        db.session.commit()
        response = self.client.get(f'/books/{book.id}/summary')
        self.assertEqual(response.status_code, 200)
        self.assertIn('summary', response.json)

    def test_get_book_summary_invalid_id(self):
        response = self.client.get('/books/999/summary')
        self.assertEqual(response.status_code, 404)

    def test_get_recommendations(self):
        # This test might need to mock the recommend_books_for_user function
        pass

    def test_generate_summary_valid(self):
        response = self.client.post('/generate-summary', json={'content': {'book_name': 'Test Book'}})
        self.assertEqual(response.status_code, 200)
        self.assertIn('summary', response.json)

    def test_generate_summary_invalid(self):
        response = self.client.post('/generate-summary', json={})
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()