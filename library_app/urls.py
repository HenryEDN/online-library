from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('Book/Detail/<int:book_id>', view=views.book_info, name='detail'),
    path('Book/Create', view=views.book_create, name='create'),
]