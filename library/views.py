from datetime import date

from django.db import IntegrityError
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import mixins


from .models import User, Book, BookShelf
from .serializers import (BookSerializer, BookShelfSerializer, UserSerializer, RegistrationSerializer,
                          CreateBookShelfSerializer)


class RegistrationView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.order_by('id')
    serializer_class = UserSerializer


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author']


class BookShelveView(viewsets.ModelViewSet):
    queryset = BookShelf.objects.all()
    serializer_class = BookShelfSerializer

    def get_queryset(self):
        user = self.request.user
        return BookShelf.objects.filter(owner=user)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        return obj

    def partial_update(self, request, pk=None):
        serializer = BookShelfSerializer(instance=BookShelf.objects.get(pk=pk), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={}, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_book_to_user(request):
    try:
        owner = User.objects.get(pk=request.user.id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not request.data.get('owner'):
        request.data['owner'] = owner.id
    serializer = CreateBookShelfSerializer(data=request.data)

    if serializer.is_valid():
        try:
            serializer.save(borrow_date=date.today())
        except IntegrityError:
            return Response(
                data={'errors': 'Book with presented id already exists in this user bookshelf.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_book_from_user(request, pk=None):
    bookshelf = BookShelf.objects.filter(owner=request.user.id, book_id=pk)
    operation = bookshelf.delete()
    data = {}
    if operation:
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
    return Response(data=data)
