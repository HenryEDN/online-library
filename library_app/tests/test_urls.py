from django.test import SimpleTestCase
from library_app.views import *
from django.urls import reverse, resolve

#Проверка привязки URL к функциям-представлениям
class TestUrls(SimpleTestCase):
    
    def test_index_url_is_resolved(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)
        
    def test_book_info_url_is_resolved(self):
        url = reverse('detail', args=['1'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, book_info)
        
    def test_book_create_url_is_resolved(self):
        url = reverse('create')
        print(resolve(url))
        self.assertEquals(resolve(url).func, book_create)
        
    