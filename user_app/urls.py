from django.urls import path
from . import views

urlpatterns = [
    path('registration', view=views.registration_view, name='registration'),
    path('login', view=views.login_view, name='login'),
    path('logout', view=views.logout_view, name='logout'),
    path('profile/<int:user_id>', view=views.userProfile, name='profile'),
    path('profile/update/<int:user_id>', view=views.profile_update, name='profile_update'),
    path('book/upvote/<int:book_id>', view=views.upvote, name='upvote'),
    path('book/downvote/<int:book_id>', view=views.downvote, name='downvote'),
    path('profile/<int:user_id>/booklist/my', view=views.booklist, name='booklist'),
    path('profile/<int:user_id>/booklist/<str:library_type>', view=views.user_libraries, name='booklist2'),
    path('book/user_status/<int:book_id>/<int:status_id>/<str:redirect_to>', view=views.give_status, name='userstatus')  
]