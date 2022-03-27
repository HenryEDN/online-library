from django.urls import path
from . import views

urlpatterns = [
    path('Registration', view=views.registration_view, name='registration'),
    path('Login', view=views.login_view, name='login'),
    path('Logout', view=views.logout_view, name='logout'),
    
]