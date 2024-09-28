from django.test import TestCase
from django.contrib.auth.models import User
from inventory.models import Item

class ItemTests(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_create_item(self):
        
        response = self.client.post('/items/', {
            'name': 'Test Item',
            'description': 'A test item description',
        }, HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_token())
        
        print(response.status_code)  
        print(response.content)      
        
        self.assertEqual(response.status_code, 201)
    
    def test_get_item(self):
        
        item = Item.objects.create(name="Test Item", description="A test item description")
        response = self.client.get(f'/items/{item.id}/', HTTP_AUTHORIZATION='Bearer ' + self.get_jwt_token())
        
        print(response.status_code)  
        print(response.content)      
        
        self.assertEqual(response.status_code, 200)

    def get_jwt_token(self):
        
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'password'})
        
        print(response.status_code)  
        print(response.content)      
        
        self.assertEqual(response.status_code, 200)
        return response.data['access']
