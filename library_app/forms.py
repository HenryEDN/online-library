from .models import Book
from django.forms import ModelForm

class BookCreationForm(ModelForm):
    class Meta:
        model = Book
        fields = ['book_title', 'book_genre', 'book_picture', 'book_description']
