from django.urls import path

from . import views


urlpatterns = [
    path('users/', views.UserView.as_view({'get': 'list'}), name='user_list'),
    path('user/<pk>', views.UserView.as_view(
        {
            'get': 'retrieve',
            'patch': 'partial_update',
            'put': 'update',
            'delete': 'destroy'
        }
    ), name='user_detail'),
    path('user/register/', views.RegistrationView.as_view(
        {
            'post': 'create'
        }
    ), name='create_user'),
    path('books/', views.BookView.as_view({'get': 'list'}), name='books_list'),
    path('book/<pk>', views.BookView.as_view(
        {
            'get': 'retrieve',
            'patch': 'partial_update',
            'put': 'update',
            'delete': 'destroy'
        }
    ), name='book_detail'),
    path('books/create_book/', views.BookView.as_view(
        {
            'post': 'create'
        }
    ), name='create_book'),
    path('user/add_book/', views.add_book_to_user),
    path('user/remove_book/<pk>', views.remove_book_from_user),
    path('user/books/', views.BookShelveView.as_view(
        {
            'get': 'list',
        }
    ), name='user_book'),
    path('user/books/<pk>', views.BookShelveView.as_view(
        {
            'put': 'update',
            'patch': 'partial_update'
        }
    ), name='update_user_book')
]
