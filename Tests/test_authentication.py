import unittest
from flask import json
from app import db
from app.ShoppingListAPI import app
from instance.config import application_config


class AuthenticationTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()

        # Binds the app to current context
        with app.app_context():
            # Create all tasbles
            db.create_all()

    def test_index(self):
        response = self.client.get('/')
        self.assertIn('This is a Shopping LIst API', response.data.decode())

    def test_signup_with_missing_credentials(self):
        """Should throw error for missing the email, name or password is empty"""
        user = json.dumps({
            'name': '',
            'email': '',
            'password': ''
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('missing the email, name or password', response.data.decode())
    def test_login_without_credentials(self):
        """Should check for empty credentials"""
        user = json.dumps({
            'email': '',
            'password': ''
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing login credentials', response.data.decode())


    def test_registration_with_invalid_email(self):
        """Should return invalid email"""
        user = json.dumps({
            'name': 'Joy',
            'email': 'candycane@gmail.com',
            'password': 'phaneroo'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid Email', response.data.decode())

    def test_registration_with_short_password(self):
        """Should return invalid email"""
        user = json.dumps({
            'name': 'Joy',
            'email': 'candy@gmail.com',
            'password': 'pha'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Make a longer Password', response.data.decode())

    def test_for_existing_email(self):
        """Should check if email exists"""
        user = json.dumps({
            'name': 'Joy',
            'email': 'candy@gmail.com',
            'password': 'phaneroo'
        })
        #self.client.post('/auth/register', data=user)
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('This email Already exists', response.data.decode())

    def test_for_successfull_registration(self):
        """Should register user successfully"""
        user = json.dumps({
            'name': 'Joy',
            'email': 'candy@gmail.com',
            'password': 'phaneroo'
        })
        response = self.client.post('/auth/register', data=user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully registered', response.data.decode())

    
    def test_login_with_invalid_email(self):
        """Should check for valid email"""
        user = json.dumps({
            'email': 'candy@gmail.com',
            'password': 'phaneroo'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Enter valid email', response.data.decode())

    def test_incorrect_login_credentials(self):
        """Should check for valid email"""

        
        self.test_successfull_registration()# first check whether the user registered
        user = json.dumps({
            'email': 'incorrect@gmail.com',
            'password': 'incorrect'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Incorrect email or password', response.data.decode())

    def test_successful_login(self):
        """Should check for valid email"""

        # first check whether the user registered
        self.test_successfull_registration()
        user = json.dumps({
            'email': 'candy@gmail.com',
            'password': 'phaneroo'
        })
        response = self.client.post('/auth/login', data=user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('You have successfully Logged in', response.data.decode())

    def test_reset_password_with_no_email(self):
        """Should thre error for non existing email"""

       
        self.test_successfull_registration()
        user = json.dumps({
            'email': ''
        })
        response = self.client.post('/auth/reset-password', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('No email sent', response.data.decode())

    def test_reset_password_for_non_exisiting_email(self):
        """Should throe error for non existing email"""

        # First of all register
        self.test_successfull_registration()
        user = json.dumps({
            'email': 'candy@gmail.com'
        })
        response = self.client.post('/auth/reset-password', data=user)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password is missing', response.data.decode())

    def tear_all_Down(self):
        
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
