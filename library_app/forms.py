from .models import Book, Chapter
from user_app.models import Comment
from django.forms import ModelForm

class BookCreationForm(ModelForm):
    class Meta:
        model = Book
        fields = ['book_title', 'book_genre', 'book_picture', 'book_description']

class ChapterCreationForm(ModelForm):
    class Meta:
        model = Chapter
        fields = ['chapter_title', 'chapter_content']

class CommentCreationForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']