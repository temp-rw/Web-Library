from rest_framework import serializers

from .models import Book, User, Genre, BookShelf


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    is_staff = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'is_staff')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=False)
    username = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'is_superuser': {'write_only': True}
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateField(required=False, read_only=True)
    queryset = User.objects.all()

    class Meta:
        model = Book
        exclude = ['owners']

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        book.save()
        return book


class CreateBookShelfSerializer(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True, required=False)
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.get_queryset(), read_only=False, required=False)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.get_queryset(), read_only=False, required=True)
    borrow_date = serializers.DateField(read_only=True, required=False)
    is_read = serializers.BooleanField(read_only=True, required=False)

    def create(self, validated_data):
        bookshelf = BookShelf.objects.create(**validated_data)
        bookshelf.save()
        return bookshelf


class BookShelfSerializer(serializers.ModelSerializer):
    borrow_date = serializers.DateField(read_only=True, required=False)
    owners = UserSerializer(many=True, read_only=True, required=False)
    book = BookSerializer(read_only=True, required=False)

    class Meta:
        model = BookShelf
        fields = '__all__'
