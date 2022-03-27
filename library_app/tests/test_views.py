from django.http import response
from django.test import TestCase, Client
from django.urls import reverse
from user_app.models import Book, Genre
from django.contrib.auth.models import User
import json

 
class TestViews(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.list_url = reverse('index')
        self.detail_url = reverse('detail', args=[1])
        self.create_url = reverse('create')
    
        self.user1 = User.objects.create_user('test', 'test@mail.com', 'testpassword')
        
        self.genre1 = Genre.objects.create(name = 'test')
        
        self.book1 = Book.objects.create(
            book_title = 'test', 
            book_picture = "library_app/static/images/4d4523c5587dc7210b9034028475262a.jpg",
            book_genre = self.genre1,
            book_description = 'test',
            book_author = self.user1,
            )
    
    #Тест GET запроса для представления index
    def test_index_view_GET(self):
        
        response = self.client.get(self.list_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'library_app/index.html')
        
    def test_detail_view_GET(self):
        
        response = self.client.get(self.detail_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'library_app/book_info.html')
        
    def test_create_view_GET(self):
        
        response = self.client.get(self.create_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'library_app/book_creation.html')
    
    
    #Позитивный тест 
    def test_create_view_Post_with_data(self):
        response = self.client.post(self.detail_url, {
            'book_title': 'test', 
            'book_picture': "library_app/static/images/4d4523c5587dc7210b9034028475262a.jpg",
            'book_genre': self.genre1,
            'book_description': 'test',
            'book_author': self.user1,
        }) 
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Book.objects.first().book_title, 'test')
        
    #Негативный тест кейс для представления "Create"    
    def test_create_view_POST_no_data(self):
        response = self.client.post(self.detail_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(Book.objects.count(), 0)