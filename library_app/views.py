from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import *
from .forms import *
from user_app.models import User_library, Profile, User_book_rate, BookStatusUser, Comment


def index(request):
    book_shelf = Book.objects.filter(book_visible = True).order_by('-book_creation_time')[:6]
    popular_book_shelf = Book.objects.filter(book_visible = True).order_by('-book_views')[:6]



    template = 'library_app/index.html' 
    context = {
        'book_shelf': book_shelf,
        'popular_book_shelf': popular_book_shelf,
        'header': 'Онлайн-библиотека любительской литературы',
    }

    return render(request, template, context)

def book_info(request, book_id):
    book = get_object_or_404(Book, id = book_id)
    chapters = Chapter.objects.filter(book = book_id).order_by('-chapter_creation_time')
    form = CommentCreationForm(request.POST, request.FILES)
    user_status = None

    comments = Comment.objects.filter(book = book).order_by('-creation_time')

    if request.user.is_authenticated:
        user_status = BookStatusUser.objects.filter(author = request.user, book = book)
    try:
        user_rate = User_book_rate.objects.get(user = request.user.id, book = book_id)
    except ObjectDoesNotExist:
        user_rate = None
    if request.user.is_authenticated:
        book.book_views += 1
        book.save(update_fields=['book_views'])

    if not user_status:
        u_status = None
    else:
        u_status = user_status[0]

    if request.method == 'POST':
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.book = book
            comment.save()
            messages.info(request, 'Комментарий успешно создан.')
            return redirect(f'/book/detail/{book_id}')

    header = f'Читать: {book.book_title}'
    
    context = {
        'book': book,
        'user_rate': user_rate,
        'header': header,
        'chapters': chapters,
        'user_status': u_status,
        'comments': comments,
        'form': form,
    }
    
    return render(request, 'library_app/book_info.html', context)

def delete_comment(request, id, book_id):
    comment = Comment.objects.get(id=id)
    if comment.author.id == request.user.id:
        comment.delete()
        messages.info(request, 'Комментарий успешно удален.')
        return redirect(f'/book/detail/{book_id}')
    return redirect(f'/book/detail/{book_id}')

def book_create(request):
    error = ''
    if request.method == 'POST':
        form = BookCreationForm(request.POST, request.FILES)
        if form.is_valid:
            try:
                book = form.save(commit=False)
                book.book_author = request.user
                book.save()
                book_title = form.cleaned_data.get('book_title')
                messages.success(request, f'Книга: {book_title} успешно создана!')
                return redirect(f'/profile/{request.user.id}/booklist/my')
            except ValueError:
                messages.info(request, 'Возможно, книга с указанным названием уже существует. Попробуйте указать другое название.')
                return redirect('create')
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
            

def library(request, sort):
    query = {
        "new": (Book.objects.all().order_by("-book_creation_time"), 'Новинки'),
        "popular": (Book.objects.all().order_by("-book_views"), 'Популярное'),
        "rates": (Book.objects.all().order_by("-book_rate"), 'Книги с высокой оценкой'),
        "all": (Book.objects.all().order_by("book_creation_time"), 'Все работы'),
    }

    books = query[sort][0]
    max_books = 9

    paginator = Paginator(books, max_books)
    page = request.GET.get('page', 1)
    try:
        page_books = paginator.page(page)
    except PageNotAnInteger:
        page_books = paginator.page(1)
    except EmptyPage:
        page_books = paginator.page(page)

    pages = paginator.count//max_books

    if pages * max_books < paginator.count:
        pages += 1
    
    list_pages = []

    for i in range(1, pages+1):
        list_pages.append(i)

    template = 'library_app/books.html'
    context = {
        'sort': sort,
        'book_shelf': page_books,
        'header': query[sort][1],
        'pages': list_pages,
        'current_page': int(page),
    }

    return render(request, template, context)


def search(request):
    
    search_query = request.GET.get('q')
    if search_query == '':
        return redirect('index')
    else:
        books = Book.objects.filter(book_title__contains = search_query).order_by('-book_creation_time')

    if not books:
        messages.success(request, f'По запросу "{search_query}" ничего не найдено.')
        return redirect('index')
    max_books = 9

    paginator = Paginator(books, max_books)
    page = request.GET.get('page', 1)
    try:
        page_books = paginator.page(page)
    except PageNotAnInteger:
        page_books = paginator.page(1)
    except EmptyPage:
        page_books = paginator.page(page)

    pages = paginator.count//max_books

    if pages * max_books < paginator.count:
        pages += 1
    
    list_pages = []

    for i in range(1, pages+1):
        list_pages.append(i)

    template = 'library_app/books.html'
    context = {
        'book_shelf': page_books,
        'header': f'Результаты поиска: {search_query}',
        'pages': list_pages,
        'current_page': int(page),
    }

    return render(request, template, context)


def jenre(request, genre):

    get_genre = Genre.objects.get(name = genre)

    books = Book.objects.filter(book_genre = get_genre.id).order_by('-book_creation_time')

    max_books = 6

    paginator = Paginator(books, max_books)
    page = request.GET.get('page', 1)
    try:
        page_books = paginator.page(page)
    except PageNotAnInteger:
        page_books = paginator.page(1)
    except EmptyPage:
        page_books = paginator.page(page)

    pages = paginator.count//max_books

    if pages * max_books < paginator.count:
        pages += 1
    
    list_pages = []

    for i in range(1, pages+1):
        list_pages.append(i)

    template = 'library_app/books.html'
    context = {
        'sort': genre,
        'book_shelf': page_books,
        'header': f'Жанр: {genre}',
        'pages': list_pages,
        'current_page': int(page),
    }

    return render(request, template, context)

def delete(request, id):
    book = Book.objects.get(id=id)
    if book.book_author.id == request.user.id:
        book.delete()
        messages.success(request, 'Вы успешно удалили книгу!')
        return redirect('index')
    else:
        messages.success(request, 'Вы не являетесь автором данной книги!')
        return redirect('index')


def update(request, id):
    book = Book.objects.get(id = id)
    template = 'library_app/update.html'
    if book.book_author.id == request.user.id:
        if request.method == 'POST':
            form = BookCreationForm(request.POST, request.FILES, instance=book)
            if form.is_valid:
                form.save()
                messages.success(request, f'Книга успешно обновлена!')
                return redirect(f'/book/detail/{id}')

    context = {
        'form': BookCreationForm(instance=book),
        'book': book,
    }    

    return render(request, template, context)


def chapter(request, book_id, chap_num):


    book = get_object_or_404(Book, id = book_id)
    try:
        chapter = Chapter.objects.filter(book = book_id).order_by('chapter_creation_time')
        
        if len(chapter)>chap_num:
            chap_next = chap_num + 1
        else:
            chap_next = False

        if chap_num - 1 > 0:
            chap_prev = chap_num - 1
        else:
            chap_prev = False   

        chap_num -= 1     


        template = 'library_app/chapter.html'
        context={
            'chapter': chapter[chap_num],
            'chap_next': chap_next,
            'chap_prev': chap_prev,
            'book': book,
        }
        return render(request, template, context)
    except IndexError:
        return redirect('index')


def chapter_create(request, book_id):

    book = Book.objects.get(id = book_id)
    other_chapters = Chapter.objects.filter(book = book_id).order_by('chapter_number')

    error = ''
    if request.method == 'POST':
        form = ChapterCreationForm(request.POST, request.FILES)
        if form.is_valid:
        
            chapter = form.save(commit=False)
            chapter.book = book
            if other_chapters:
                chapter.chapter_number = other_chapters[0].chapter_number
            else:
                chapter.chapter_number = 1
            chapter.save()
            chapter_title = form.cleaned_data.get('chapter_title')
            messages.success(request, f'Глава "{chapter_title}" для книги "{book.book_title}" успешно создана!')
            return redirect(f'/book/{book_id}/chapter/create')
        else:
            error = 'Form is invalid'
    
    
    form = ChapterCreationForm
    context = {
        'title': 'Create post',
        'form': form,
        'error': error,
        'book': book,
        'header': 'Создание главы',

    }
    template = 'library_app/chapter_creation.html'
    return render(request, template, context)