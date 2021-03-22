from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=255, verbose_name='Username')
    email = models.EmailField(unique=True, max_length=255, verbose_name='Email')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username


class Genre(models.Model):
    CATEGORIES = [
        ('deleted', 'Deleted'),
        ('detective', 'Detective'),
        ('adventure', 'Adventure'),
        ('sci-fi', 'Sci-Fi'),
        ('documentary', 'Documentary'),
        ('humor', 'Humor'),
        ('fantasy', 'Fantasy'),
        ('horror', 'Horror')
    ]

    name = models.CharField(max_length=200, choices=CATEGORIES, verbose_name='Genre')

    def __str__(self):
        return self.name


def get_sentinel_genre():
    return Genre.objects.get_or_create(name=Genre.CATEGORIES[0])


class Book(models.Model):
    cover = models.CharField(max_length=255, verbose_name='BookCover')
    title = models.CharField(max_length=255, verbose_name='Title')
    author = models.CharField(max_length=255, verbose_name='Author')
    source_link = models.CharField(max_length=255, verbose_name='SourceLink')
    genre = models.ForeignKey(
        'Genre',
        on_delete=models.SET(get_sentinel_genre),
        verbose_name='Genre'
    )
    description = models.TextField(verbose_name='Description')
    creation_date = models.DateField(auto_now_add=True, verbose_name='CreationDate')
    owners = models.ManyToManyField(User, related_name='books', through='BookShelf', through_fields=['book', 'owner'])

    def __str__(self):
        return self.title


class BookShelf(models.Model):
    borrow_date = models.DateField(auto_now_add=True, verbose_name='BorrowDate')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, verbose_name='Book')
    owner = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name='Owner')
    is_read = models.BooleanField(default=False, verbose_name='IsRead')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['book', 'owner'], name='unique book')
        ]
        verbose_name_plural = 'Book shelves'
        verbose_name = 'Book shelf'
