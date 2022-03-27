from django.contrib import admin
from .models import Book_Status, Profile, User_library

admin.site.register(Book_Status)
admin.site.register(Profile)
admin.site.register(User_library)
