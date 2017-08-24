import unittest
from flask import json
from app import db
from app.ShoppingListAPI import app
from instance.config import application_config

class ShoppingListTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()

        # Binds the app to current context
        with app.app_context():
            # Creating all tables
            db.create_all()

        user = json.dumps({
            'name': 'Joy',
            'email': 'candycane@gmail.com',
            'password': 'phaneroo'
        })
        response = self.client.post('/auth/register', data=user)
        json_repr = json.loads(response.data.decode())
        self.token = json_repr['id']

    def test_add_list_without_list_name(self):
        """Should return  error code 400 for missing list name"""
        mylist = json.dumps({
            'nameoflist': ''
            
        })
        response = self.client.post('/shoplists', data=mylist,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing list name', response.data.decode())

    def test_add_list_successfully(self):
        """Should return OK for  added"""
        mylist = json.dumps({
            'nameoflist': 'JOY_wedding',
        
        })
        response = self.client.post('/shoplists', data=mylist,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('List added Successfully', response.data.decode())

    def test_add_list_with_existing_list_name(self):
        """Should return 400 for missing list name"""

        
        self.test_add_list_successfully()
        mylist = json.dumps({
            'nameoflist': 'Travel',
            
        })
        response = self.client.post('/shoplists', data=mylist,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('This list name Already exists', response.data.decode())

    def test_get_list_when_nolists_exist(self):
        """Should return all  lists"""
        response = self.client.get('/shoplists',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('No Shopping Lists has been created',
                      response.data.decode())

    def test_get_list(self):
        """Should return all  lists"""

       
        self.test_add_list_successfully()#first test for adding bucket
        response = self.client.get('/shoplists',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Debbieshopping',
                      response.data.decode())

    def test_get_bucket_search(self):
        """ return OK and the list"""

        
        self.test_add_list_successfully()
        response = self.client.get('/mylist?q=Debbieshopping',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Debbieshopping',
                      response.data.decode())

    def test_get_single_bucket(self):
        """ return OK and the list"""

        
        self.test_add_bucket_successfully()
        response = self.client.get('/buckets/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Travel',
                      response.data.decode())

    def test_get_single_list_with_no_lists_availble(self):
        """Should return code 400 if no lists exist"""

        response = self.client.get('/mylist/1',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('list not found',
                      response.data.decode())

    def test_get_nonexisting_single_list(self):
        """Should return 400 list doesnt exists"""

        
        self.test_add_list_successfully()
        response = self.client.get('/mylist/6',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('The list with Id 6 is not found',
                      response.data.decode())

    def test_get_single(self):
        """Should return a single list"""

        
        self.test_add_list_successfully()
        response = self.client.get('/mylist/2',
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Christmas',
                      response.data.decode())

    def test_update_list_which_doesnt_exist(self):
        """
        Should return 400 list
        does not exists
        """

       
        self.test_add_lisy_successfully()
        mylist = json.dumps({
            'nameoflist': 'Travel to paris',
            
        })
        response = self.client.put('/mylist/2', data=shoplists,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('list does not exist', response.data.decode())

    def test_update_list_without_list_name(self):
        """Should return 400 for missing list name"""
        mylist = json.dumps({
            'nameoflist': '',
            
        })
        response = self.client.put('/mylist/4', data=shoplists,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing list name', response.data.decode())

    def test_update_list_successfully(self):
        """Should return ok """

        
        self.test_add_list_successfully()
        bucket = json.dumps({
            'nameoflist': 'Food',
           
        })
        response = self.client.put('/mylist/1', data=shoplists,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Food', response.data.decode())

    def test_delete_list_that_doesnt_exist(self):
        

        response = self.client.delete(
            '/mylist/1', headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('list missing', response.data.decode())

    def test_delete_list_successfully(self):
        """Should return OK for bucket added"""

        
        self.test_add_list_successfully()
        response = self.client.delete(
            '/mylist/1', headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('List deleted successfully', response.data.decode())

    def tear_all_Down(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
