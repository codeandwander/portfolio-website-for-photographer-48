import unittest
from unittest.mock import patch
from flask import url_for
from app import app
from models import Photo, Category, Contact

class TestPortfolioWebsite(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to the Portfolio Website', response.data)

    def test_about_page(self):
        response = self.app.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About the Photographer', response.data)

    def test_categories_page(self):
        response = self.app.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Photo Galleries', response.data)

    def test_category_page(self):
        # Create a test category and photos
        category = Category(name='Portraits')
        photo1 = Photo(title='Portrait 1', category=category)
        photo2 = Photo(title='Portrait 2', category=category)

        response = self.app.get('/category/portraits')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Portrait 1', response.data)
        self.assertIn(b'Portrait 2', response.data)

    def test_contact_page(self):
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book a Photoshoot', response.data)

    def test_contact_form_submission(self):
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'message': 'Hi, I would like to book a photoshoot.'
        }
        response = self.app.post('/contact', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Thank you for your message!', response.data)

        # Check if the contact is saved to the database
        contact = Contact.query.filter_by(name='John Doe').first()
        self.assertIsNotNone(contact)
        self.assertEqual(contact.email, 'john@example.com')
        self.assertEqual(contact.message, 'Hi, I would like to book a photoshoot.')

    @patch('models.Photo.get_all')
    def test_photo_gallery(self, mock_get_all):
        # Mock the Photo.get_all() method to return test data
        mock_get_all.return_value = [
            Photo(title='Photo 1', category=Category(name='Portraits')),
            Photo(title='Photo 2', category=Category(name='Landscapes')),
            Photo(title='Photo 3', category=Category(name='Events'))
        ]

        response = self.app.get('/gallery')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Photo 1', response.data)
        self.assertIn(b'Photo 2', response.data)
        self.assertIn(b'Photo 3', response.data)

if __name__ == '__main__':
    unittest.main()