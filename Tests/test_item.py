import unittest
from flask import json
from app import db
from app.ShoppingListAPI import app
from instance.config import application_config

class ItemTestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object(application_config['TestingEnv'])
        self.client = app.test_client()

        
        with app.app_context():
            # Create all tables
            db.create_all()

        user = json.dumps({
            'name': 'Joy',
            'email': 'candycane@gmail.com',
            'password': 'phaneroo'
        })
        response = self.client.post('/auth/register', data=user)
        json_repr = json.loads(response.data.decode())
        self.token = json_repr['id']

    def test_add_item_with_no_name(self):
        """Should return 400 for missing item name"""
        item = json.dumps({
            'nameofitem': ''
            'priceofitem':'3000'
            
            
            })
        response = self.client.post('/mylist/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing Item name', response.data.decode())

    def test_add_item_when_list_doesnt_exist(self):
        """Should return 400 for missing list"""
        item = json.dumps({
            'nameofitem': 'Travel to paris'
            'priceofitem':2000
            })
        response = self.client.post('/mylist/3/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('List not found', response.data.decode())

    def test_add_item_successfully(self):
        """Should return 201 for item added"""

        
        shoplists = json.dumps({
            'nameoflist': 'Go to Nairobi'
        })
        self.client.post('/mylist', data=shoplists,
                         headers={"Authorization": self.token})

        item = json.dumps({
            
            'nameofitem': 'Travel tp paris',
            'priceofitem': '7000'
            
            })
        response = self.client.post('/mylist/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn(' Item Successfully Added ', response.data.decode())

    def test_add_existing_item(self):
        """Should return 400 for duplicate item"""
        
        self.test_add_item_successfully()
        
        item = json.dumps({
            'nameofitem': 'Go to Nairobi'
            'priceof item':500
            })
        response = self.client.post('/mylist/1/items', data=item,
                                    headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('item name Already exists', response.data.decode())

    def test_edit_item_with_no_name(self):
        """Should return 400 for missing item name"""

        item = json.dumps({
            'nameofitem': ''
            'priceofitem':500
            
            })
        response = self.client.put('/buckets/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing Item name', response.data.decode())


        def test_edit_item_with_no_price(self):
        """Should return 400 for missing item price"""

        item = json.dumps({
            'nameofitem':'wedding'
            'priceofitem':''
            
            })
        response = self.client.put('/mylists/1/items/4', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing Item price', response.data.decode())

    def test_edit_item_with_no_list(self):
        """Should return 400 for no list"""

        item = json.dumps({'item': 'Dubai shopping'})
        response = self.client.put('/mylist/3/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('list  not found', response.data.decode())

    def test_edit_item_with_no_item(self):
        """Should return 400 for missing item"""

        # First of all add the bucket
        shoplists = json.dumps({
            'mylist': 'Travel',
            
        })
        self.client.post('/mylist', data=shoplists,
                         headers={"Authorization": self.token})
        item = json.dumps({
            'nameofitem': 'Go to New York'
            'priceofitem':1000
            })
        response = self.client.put('/mylist/2/items/4', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('item with id 4 does not exist',
                      response.data.decode())

    def test_edit_item_succesfully(self):
        """Should return OK for item edited"""

        self.test_add_item_successfully()
        item = json.dumps({
            'item': 'Go to Silicon Valley'
            })
        response = self.client.put('/mylist/1/items/1', data=item,
                                   headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Successfully updated item', response.data.decode())
        #self.assertIn('Go to Silicon Valley', response.data.decode())

    def test_delete_item_that_doesnt_exist(self):
        """Should return 400 for missing item"""

        
        response = self.client.delete('/mylist/1/items/6',
                                      headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Item with id 6 does not exist', response.data.decode())

    def test_delete_item_successfully(self):
        """Should return 201 for item deleted"""

        self.test_add_item_successfully()
        response = self.client.delete('/mylist/1/items/2',
                                      headers={"Authorization": self.token})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Item 2 successfully deleted', response.data.decode())

    def tear_all_Down(self):
        # Drop all tables
        with app.app_context():
            # Drop all tables
            db.session.remove()
            db.drop_all()


if __name__ == '__main__':
    unittest.main()
