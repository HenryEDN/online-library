from django.urls import path
from . import views

urlpatterns = [
    path('', view=views.index, name='index'),
    path('library/genre/<str:genre>', view=views.jenre, name='genre'),
    path('book/detail/<int:book_id>', view=views.book_info, name='detail'),
    path('book/create', view=views.book_create, name='create'),
    path('library/<str:sort>', view=views.library, name='library'),
    path('search/', view=views.search, name='search_query'),
    path('book/delete/<int:id>', view=views.delete, name='delete'),
    path('book/update/<int:id>', view=views.update, name='update'),
    path('book/<int:book_id>/chapter/create', view=views.chapter_create, name='create_chapter'),
    path('book/<int:book_id>/chapter/<int:chap_num>', view=views.chapter, name='chapter'),
    path('comment/delete/<int:id>/<int:book_id>', view=views.delete_comment, name='del_com'),
]