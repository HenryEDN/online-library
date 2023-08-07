from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField

#Cущность Жанр
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
    
#Сущность Книга
class Book(models.Model):
    book_title = models.CharField(max_length=60, unique=True)
    book_genre = models.ForeignKey(Genre, on_delete=CASCADE)
    book_picture = models.ImageField(null = True, blank=True, upload_to='images/')
    book_description = RichTextField(blank=True, null=True)
    book_author = models.ForeignKey(User, on_delete=models.CASCADE)
    book_creation_time = models.DateTimeField(auto_now=True)
    book_rate = models.IntegerField(default=0)
    book_views = models.IntegerField(default=0)
    book_visible = models.BooleanField(default = False)

    def __str__(self):
        return self.book_title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

#Cущность глава
class Chapter(models.Model):
    chapter_title = models.CharField(max_length=60)
    chapter_content = RichTextField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=CASCADE)
    chapter_creation_time = models.DateTimeField(auto_now=True)
    chapter_number = models.IntegerField(null=True)
    chapter_visible = models.BooleanField(default = False)

    def __str__(self):
        return self.chapter_title

    class Meta:
        verbose_name = "Глава"
        verbose_name_plural = "Главы"





