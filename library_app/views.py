from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from .models import *
from .forms import *
from user_app.models import User_library, Profile


def index(request):
    book_shelf = Book.objects.order_by('-book_creation_time')[:6]
    template = 'library_app/index.html'

    context = {
        'book_shelf': book_shelf,
        'header': 'Онлайн-библиотека любительской литературы',
    }

    return render(request, template, context)

def book_info(request, book_id):
    book = get_object_or_404(Book, id = book_id)
    if request.user.is_authenticated:
        book.book_views += 1
        book.save(update_fields=['book_views'])

    header = f'Читать: {book.book_title}'
    
    context = {
        'book': book,
        'header': header,
    }
    
    return render(request, 'library_app/book_info.html', context)

def book_create(request):
    error = ''
    if request.method == 'POST':
        form = BookCreationForm(request.POST, request.FILES)
        if form.is_valid:
            book = form.save(commit=False)
            book.book_author = request.user
            book.save()
            return redirect('index')
        else:
            error = 'Form is invalid'
    form = BookCreationForm
    context = {
        'title': 'Create post',
        'form': form,
        'error': error,
        'header': 'Создание книги',
    }
    template = 'library_app/book_creation.html'
    return render(request, template, context)
            