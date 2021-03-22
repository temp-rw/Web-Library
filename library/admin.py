from django.contrib import admin
from .models import Book, User, Genre, BookShelf


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'creation_date']
    ordering = ('id',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ('id',)


@admin.register(BookShelf)
class BookShelfAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'book', 'borrow_date', 'is_read']
    ordering = ('id',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_superuser', 'is_staff']
    ordering = ('id',)
