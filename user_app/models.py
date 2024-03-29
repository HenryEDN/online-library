from django.db import models
from library_app.models import Genre, Book, Chapter
from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ckeditor.fields import RichTextField

class Book_Status(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Статус"
        verbose_name_plural = "Статусы"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, null=False)
    nickname = models.CharField(max_length=50, default="User")
    about_user = RichTextField(blank=True, null=True)
    profile_picture =  models.ImageField(null = True, blank=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    #Signals

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        instance.profile.save()

class User_library(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE)
    book = models.ForeignKey(Book, on_delete=CASCADE)
    book_status = models.ForeignKey(Book_Status, on_delete=CASCADE)
    add_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"библиотека self.owner.user.username"

    class Meta:
        verbose_name = "Библиотека"
        verbose_name_plural = "Библиотеки"


class User_book_rate(models.Model):


    user = models.ForeignKey(User, on_delete=CASCADE, null=False)
    book = models.ForeignKey(Book, on_delete=CASCADE, null=False)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return f"оценка {self.user} книге '{self.book}'"

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки" 

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE)
    book = models.ForeignKey(Book, on_delete=CASCADE)
    text = RichTextField(blank=True, null=True)
    creation_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'({self.book}) Comment {self.id} by {self.author}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

class BookStatusUser(models.Model):
    author = models.ForeignKey(User, on_delete=CASCADE)
    book = models.ForeignKey(Book, on_delete=CASCADE)
    status = models.ForeignKey(Book_Status, on_delete=CASCADE)
    creation_time = models.DateField(auto_now=True)


    
    class Meta:
        verbose_name = 'Статус пользователя'
        verbose_name_plural = 'Статусы пользователя'