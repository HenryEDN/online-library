from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django.contrib import messages

from .forms import *
from .models import *


def registration_view(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Пользователь " + user + " был успешно создан!")
            return redirect('login')

            
    context = {
		'form': form,
        'header': 'Регистрация',
	}
    return render(request, 'user_app/registration.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Логин или пароль введен неверно')

    context = {
        'header': 'Авторизация',
    }
    return render(request, 'user_app/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')


def userProfile(request, user_id):
    user = get_object_or_404(User, id = user_id)
    user_info = Profile.objects.get(user = user_id)
    books = Book.objects.filter(book_author = user_id).order_by('-book_creation_time')

    status = Book_Status.objects.all()

    in_plans = BookStatusUser.objects.filter(status = status[1], author = user).order_by('-creation_time')
    red = BookStatusUser.objects.filter(status = status[0], author = user).order_by('-creation_time')
    read = BookStatusUser.objects.filter(status = status[2], author = user).order_by('-creation_time')

    template = 'user_app/profile.html'

    context = {
        'header': 'Страница пользователя',
        'user': user,
        'books': books,
        'user_info': user_info,
        'in_plans': in_plans,
        'red': red,
        'read': read,
    }

    return render(request, template, context)

def upvote(request, book_id):
    book = Book.objects.get(id = book_id)
    
    try:
        user_rate = User_book_rate.objects.get(user = request.user.id, book = book_id)
    except ObjectDoesNotExist:
        user_rate = None

    if user_rate != None:
        if user_rate.rate == 0:
            user_rate.rate = 1
            book.book_rate += 1
        elif user_rate.rate == 2:
            book.book_rate += 2
            user_rate.rate = 1
        else:
            user_rate.rate = 0
            book.book_rate -= 1
        user_rate.save(update_fields=['rate'])
        book.save(update_fields=['book_rate'])
        return redirect(f'/book/detail/{book_id}')
    else:
        user_rate = User_book_rate(user = request.user, book = book, rate = '1')
        book.book_rate += 1
        book.save(update_fields=['book_rate'])
        user_rate.save()
        return redirect(f'/book/detail/{book_id}')

def downvote(request, book_id):
    book = Book.objects.get(id = book_id)
    
    try:
        user_rate = User_book_rate.objects.get(user = request.user.id, book = book_id)
    except ObjectDoesNotExist:
        user_rate = None

    if user_rate != None:
        if user_rate.rate == 0:
            book.book_rate -= 1
            user_rate.rate = 2
        elif user_rate.rate == 1:
            book.book_rate -= 2
            user_rate.rate = 2
        else:
            user_rate.rate = 0
            book.book_rate += 1
        user_rate.save(update_fields=['rate'])
        book.save(update_fields=['book_rate'])
        return redirect(f'/book/detail/{book_id}')
    else:
        user_rate = User_book_rate(user = request.user, book = book, rate = '2')
        book.book_rate -= 1
        user_rate.save()
        book.save(update_fields=['book_rate'])
        return redirect(f'/book/detail/{book_id}')

def booklist(request, user_id):

    if request.user.id == user_id:
        user = User.objects.get(id = user_id)
        search_query = request.GET.get('q')
        if search_query == None:
            books = Book.objects.filter(book_author = user_id).order_by('-book_creation_time')
        else:
            books = Book.objects.filter(book_title__contains = search_query, book_author = user_id).order_by('-book_creation_time')
            if not books:
                messages.success(request, f'Книги с названием "{search_query}" не найдены.')
                books = Book.objects.filter(book_author = user_id).order_by('-book_creation_time')

        

        if request.method == 'POST':
            id_list = request.POST.getlist('boxes')

            books.update(book_visible=False)


            for id in id_list:
                Book.objects.filter(pk=int(id)).update(book_visible=True)

            messages.success(request, 'Изменения были применены!')
            return redirect(f'/profile/{request.user.id}/booklist/my')

    else:
        return redirect('index')

    template = 'user_app/user_library.html'

    context = {
        'header': 'Ваши книги',
        'user': user,
        'books': books,
    }

    return render(request, template, context)


def profile_update(request, user_id):
    profile = Profile.objects.get(user = user_id)
    template = 'user_app/profile_update.html'
    print(profile.user, user_id)
    if profile.user.id == request.user.id:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
            if form.is_valid:
                form.save()
                messages.success(request, f'Профиль успешно обновлен!')
                return redirect(f'/profile/{user_id}')
    else:
        return redirect('index')
    context = {
        'form': ProfileUpdateForm(instance=profile),
        'profile': profile,
    }    

    return render(request, template, context)

def give_status(request, book_id, status_id, redirect_to):

    book = Book.objects.get(id = book_id)

    #1 - Прочитано
    #2 - В планах
    #3 - Читает
    status = Book_Status.objects.all()

    redirect_list = {
        '1': f'/book/detail/{book_id}',
        '2': f'/profile/{request.user.id}',
        '3': f'/profile/{request.user.id}/booklist/in_plans',
        '4': f'/profile/{request.user.id}/booklist/red',
        '5': f'/profile/{request.user.id}/booklist/read',
    }

    user_status = BookStatusUser.objects.filter(author = request.user, book = book)
    if not user_status:
        user_status = BookStatusUser(author = request.user, book = book, status = status[status_id])
        user_status.save()
        messages.info(request, f'Вы добавлили книгу "{book.book_title}" в список "{status[status_id].name}"')
        return redirect(f'/book/detail/{book_id}')
    elif user_status[0].status == status[status_id]:
        messages.info(request, f'Вы убрали книгу "{book.book_title}" из списка "{status[status_id].name}"')
        user_status.delete()
        return redirect(redirect_list[redirect_to])
    else:
        user_status.delete()
        user_status = BookStatusUser(author = request.user, book = book, status = status[status_id])
        user_status.save()
        messages.info(request, f'Вы добавлили книгу "{book.book_title}" в список "{status[status_id].name}"')
        return redirect(redirect_list[redirect_to])
    
    
def user_libraries(request, user_id, library_type):

    #1 - Прочитано
    #2 - В планах
    #3 - Читает

    status = Book_Status.objects.all()
    user = User.objects.get(id = user_id)

    type_tuple ={
        'in_plans': (BookStatusUser.objects.filter(status = status[1], author = user).order_by('-creation_time'),'В планах',3, '1'),
        'red': (BookStatusUser.objects.filter(status = status[0], author = user).order_by('-creation_time'),'Прочитано',4, '0'),
        'read': (BookStatusUser.objects.filter(status = status[2], author = user).order_by('-creation_time'),'Читаю',5, '2'),
    }

    template = 'user_app/user_libraries.html'


    context = {
    'header': type_tuple[library_type][1],
    'books': type_tuple[library_type][0],
    'redirect': str(type_tuple[library_type][2]),
    'key': type_tuple[library_type][3],
    }

    return render(request, template, context)